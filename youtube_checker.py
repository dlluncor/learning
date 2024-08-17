import os
import json

from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


upload_playlist_id = os.environ.get('UPLOAD_PLAYLIST_ID')

# Replace with your API key or OAuth credentials
api_key = os.environ.get('YOUTUBE_API_KEY')
client_secret_file = 'client_secret.json'

def get_uploaded_videos_with_oauth(api_key):

	scopes = ["https://www.googleapis.com/auth/youtube.readonly"]  # Adjust scopes as needed

	flow = InstalledAppFlow.from_client_secrets_file(
	    "client_secret.json", scopes)
	auth_url, state = flow.authorization_url(access_type='offline', prompt='consent')

	creds = Credentials.from_authorized_user_file(
	client_secret_file, ['https://www.googleapis.com/auth/youtube.readonly'])

	youtube = build('youtube', 'v3', credentials=creds)

	# Get channel information to retrieve uploads playlist ID
	request = youtube.channels().list(
	  part="contentDetails",
	  mine=True
	)
	response = request.execute()
	uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

	# Get uploaded videos
	request = youtube.playlistItems().list(
		part="snippet",
		playlistId=uploads_playlist_id,
		maxResults=10  # Adjust max results as needed
	)
	response = request.execute()

	videos = []
	for item in response['items']:
		video = {
			'title': item['snippet']['title'],
			'description': item['snippet']['description'],
			# Add other desired video information
		}
		videos.append(video)

	return videos

# Example usage
#my_videos = get_uploaded_videos_with_oauth(api_key)
#for video in my_videos:
#	print(video['title'])

def get_uploaded_videos(filename, debug):
	with open(filename) as f:
		obj = json.loads(f.read())

	titles = set([])
	total_results = obj['pages'][0]['pageInfo']['totalResults']
	missing_positions = set([i for i in range(total_results)])

	for page in obj['pages']:
		for item in page['items']:
			snippet = item['snippet']
			pos = snippet['position']
			titles.add(snippet['title'])
			if pos in missing_positions:
				missing_positions.remove(pos)

	if debug:
		print(titles)
		print('There are {} videos uploaded'.format(len(titles)))
		print('Missing positions')
		print(missing_positions)
	return {
		'titles': titles
	}

def get_video_files(folder_path):
	extensions = ['.mp4', '.mov']
	video_filenames = []
	for root, dirs, files in os.walk(folder_path):
		for rel_path in files:
			filename, ext = os.path.splitext(rel_path)
			if ext.lower() not in extensions:
				continue
			video_filenames.append(filename)

	return video_filenames

def is_file_uploaded(filename, uploaded_titles):
	for title in uploaded_titles:
		if filename in title:
			return True

	return False

def get_videos_not_uploaded_yet(uploaded_video_obj, video_filenames):
	# Youtube removes the underscore and turns it into a space
	uploaded_titles = [title.replace(' ', '_') for title in uploaded_video_obj['titles']]
	missing_files_to_upload = []

	for filename in video_filenames:

		if is_file_uploaded(filename, uploaded_titles):
			continue

		missing_files_to_upload.append(filename)

	return missing_files_to_upload

def main():
	debug = False
	videos_obj = get_uploaded_videos(filename='channel_videos_list.json', debug=debug)
	video_filenames = get_video_files(folder_path='/Users/dlluncor/Downloads/david_large_videos_250')

	print('I tried to upload {} videos'.format(len(video_filenames)))

	missing_files_to_upload = get_videos_not_uploaded_yet(videos_obj, video_filenames)

	if not missing_files_to_upload:
		print('All files are uploaded!!')
	else:
		print('These videos arent uploaded yet')
		print(missing_files_to_upload)

if __name__ == '__main__':
	main()

