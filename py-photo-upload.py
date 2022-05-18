import sys
import pickle
import os.path
import requests
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def upload(token ,file):
	f = open(file, 'rb').read()
	print(sys.getsizeof(f))
	url = 'https://photoslibrary.googleapis.com/v1/uploads'
	headers = {
		'Authorization': "Bearer " + token,
		'Content-Type': 'application/octet-stream',
		# 'X-Goog-Upload-Content-Type': 'image/png',
		'X-Goog-Upload-Protocol': "raw",
	}

	r = requests.post(url, data=f, headers=headers)
	return r.content
def createItem(token, upload_token):
	url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'
	body = {
		'newMediaItems' : [
			{
				"description": "test upload",
				"simpleMediaItem": {
					"uploadToken": upload_token.decode()
				}
			}
		]
	}
	body_data = json.dumps(body)
	
	headers = {
		'Authorization': "Bearer " + token,
		'Content-Type': 'application/json'
	}
	r = requests.post(url, data=body_data, headers=headers)
	return r.content

def main():
	credentialsFile = 'credentials.json'  # Please set the filename of credentials.json
	pickleFile = 'token.pickle'  # Please set the filename of pickle file.


	SCOPES = ['https://www.googleapis.com/auth/photoslibrary']
	creds = None
	token = ''
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
	data_token = upload(creds.token, '1.png')
	print(data_token)
	upload_item = createItem(creds.token, data_token)
	print(upload_item)
	

if __name__ == '__main__':
	main()