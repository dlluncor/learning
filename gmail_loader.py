import mailbox
import os
import json
import datetime
import time

from dateutil import parser as dparser
from typing import List, Dict, TypedDict

# Specify the path to your .mbox folder
cfg1 = {
    'root_dir': '/Users/dlluncor/Desktop/Code/davids_emails/all',
    'mbox_path': '/Users/dlluncor/Downloads/David_AllMail.mbox'
}

cfg2 = {
    'root_dir': '/Users/dlluncor/Desktop/Code/davids_emails/starred',
    'mbox_path': '/Users/dlluncor/Downloads/Starred_Takeout/Starred.mbox'
}

cfg3 = {
    'root_dir': '/Users/dlluncor/Desktop/Code/davids_emails/10mb',
    'mbox_path': '/Users/dlluncor/Downloads/Takeout/Mail/LargeEmails-10MB.mbox'
}

cfg4 = {
    'root_dir': '/Users/dlluncor/Desktop/Code/davids_emails/5mb',
    'mbox_path': '/Users/dlluncor/Downloads/Takeout_2/Mail/LargeEmails-5MB.mbox'
}

cfg5 = {
    'root_dir': '/Users/dlluncor/Desktop/Code/davids_emails/1mb',
    'mbox_path': '/Users/dlluncor/Downloads/LargeEmails-1MB-001.mbox'
}

SHOULD_WRITE_ATTACHMENTS = True
cfg = cfg3

AttachmentDict = TypedDict('AttachmentDict', {
    'content': bytes,
    'filename': str
})

def parse_attachments(message) -> List[AttachmentDict]:
    if message.get_content_maintype() != 'multipart':
        return []

    attachments = []
    for part in message.walk():
        if part.get_content_maintype() == 'multipart': continue
        if part.get('Content-Disposition') is None: continue

        filename = part.get_filename()
        if filename is None or filename == 'None':
            continue

        contents = part.get_payload(decode=True)

        #print('Have an attachment')
        #import pdb; pdb.set_trace()
        #print(filename)

        date_str = message['Date']
        dt = dparser.parse(date_str)

        # Group months together
        rel_path = '{:02d}_{:02d}/{}'.format(dt.year, dt.month, filename)

        attachments.append({
            'content': contents,
            'rel_path': rel_path,
            'filename': filename
        })

    return attachments

def get_multipart_text_body(message):
    assert message.get_content_maintype() == 'multipart'
    for part in message.walk():
        if type(part.get_payload()) == str:
            return part.get_payload()

    return 'unknown'

def write_attachments(cfg: Dict, attachments: List[AttachmentDict]) -> None:
    if not attachments:
        return

    for attachment in attachments:
        full_path = os.path.join(cfg['root_dir'], attachment['rel_path'])
        dir_path = os.path.dirname(full_path)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(full_path, 'wb') as f:
            f.write(attachment['content'])

class EmailMessage(object):

    def __init__(self, message):
        self.message = message

    def get_text_body(self) -> str:
        message = self.message
        if message.is_multipart():
            return get_multipart_text_body(message)
        else:
            return message.get_payload()

    def get_json_payload(self) -> Dict:
        message = self.message
        return {
            'subject': message['subject'],
            'from': message['from'],
            'body': self.get_text_body(),
            'attachments': []
        }

    def get_attachments(self) -> List[AttachmentDict]:
        if not self.message.is_multipart():
            return []

        return parse_attachments(self.message)

    def print_attrs(self) -> str:
        # Access message attributes
        subject = message["subject"]
        sender = message["from"]

        # Do something with the message data
        print("Subject:", subject)
        print("Sender:", sender)   
        print('Body: ', self.get_text_body()) 

    @staticmethod
    def create(message):
        return EmailMessage(message)

def main():

    # Open the mbox folder
    mbox = mailbox.mbox(cfg['mbox_path'])
    print('Opening mbox folder {}'.format(cfg['mbox_path']))

    # Iterate through each message in the folder
    MAX = 10000000
    payloads = []
    num_emails = 0
    before = time.time()
    should_write_attachments = SHOULD_WRITE_ATTACHMENTS

    if not should_write_attachments:
        print('Skipping writing attachments out to separate files nested in folders')

    for message in mbox:
        num_emails += 1
        if num_emails > MAX:
            break

        msg_obj = EmailMessage.create(message)
        payload = msg_obj.get_json_payload()
        attachments = msg_obj.get_attachments()

        if attachments:
            if should_write_attachments:
                write_attachments(cfg, attachments)
            payload['attachments'] = [attach['rel_path'] for attach in attachments]

        payloads.append(payload)

    after = time.time()

    # Write out 2000 emails at a time
    chunk_size = 2000 #2000
    chunks = [payloads[i:i + chunk_size] for i in range(0, len(payloads), chunk_size)]
    i = 0
    for chunk in chunks:
        with open(os.path.join(cfg['root_dir'], 'emails-{}.json'.format(i)), 'w') as f:
            f.write(json.dumps({
                'emails': chunk
            }, indent=2))

        i += 1

    print('Took {:.2f} seconds to process {} emails'.format(after - before, num_emails))


if __name__ == '__main__':
    main()
