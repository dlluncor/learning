import mailbox
import os
import json
import datetime

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

cfg = cfg2

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
        contents = part.get_payload(decode=True)

        #print('Have an attachment')
        #import pdb; pdb.set_trace()
        #print(filename)

        date_str = message['Date']
        dt = dparser.parse(date_str)

        # Group months together
        rel_path = '{}_{}/{}'.format(dt.month, dt.year, filename)

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
    print('About to open mbox folder')

    # Open the mbox folder
    mbox = mailbox.mbox(cfg['mbox_path'])
    print('Opened mbox folder {}'.format(cfg['mbox_path']))

    # Iterate through each message in the folder
    MAX = 1000
    payloads = []
    num_emails = 0
    for message in mbox:
        num_emails += 1
        if num_emails > MAX:
            break

        msg_obj = EmailMessage.create(message)
        payload = msg_obj.get_json_payload()
        attachments = msg_obj.get_attachments()

        if attachments:
            write_attachments(cfg, attachments)
            payload['attachments'] = [attach['rel_path'] for attach in attachments]

        payloads.append(payload)

    # Write out 2000 emails at a time
    with open(os.path.join(cfg['root_dir'], 'out-0.json'), 'w') as f:
        f.write(json.dumps({
            'emails': payloads
        }))

    print('Successfully processed {} emails'.format(num_emails))


if __name__ == '__main__':
    main()
