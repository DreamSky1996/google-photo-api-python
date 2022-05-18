import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def main():
	credentialsFile = 'credentials.json'  # Please set the filename of credentials.json
	pickleFile = 'token.pickle'  # Please set the filename of pickle file.

	SCOPES = ['https://www.googleapis.com/auth/photoslibrary']
	creds = None
	if os.path.exists(pickleFile):
		with open(pickleFile, 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				credentialsFile, SCOPES)
			creds = flow.run_local_server()
		with open(pickleFile, 'wb') as token:
			pickle.dump(creds, token)

	service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
	results = service.mediaItems().list(pageSize=10).execute()
	items = results.get('mediaItems', [])
	print(len(items))
	for item in items:
		print(item)

	# Call the Photo v1 API
	# results = service.albums().list(
	# 	pageSize=10, fields="nextPageToken,albums(id,title)").execute()
	# items = results.get('albums', [])
	# if not items:
	# 	print('No albums found.')
	# else:
	# 	print('Albums:')
	# 	for item in items:
	# 		print('{0} ({1})'.format(item['title'].encode('utf8'), item['id']))


if __name__ == '__main__':
	main()