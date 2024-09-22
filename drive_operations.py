import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from authenticator import authenticate
from datetime import datetime

service = authenticate()


def listFiles():
    results = service.files().list(
        fields= "files(name, mimeType, modifiedTime)"
    ).execute()
    items = results.get('files', [])
    print(items)
    if items == None:
        print('No files found')
    else:
        print('Files:')
        for item in items:
            name = item['name']
            mime_type = item['mimeType']
            modified_time = datetime.strptime(item['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_time = modified_time.strftime("%Y-%m-%dT%H:%M:%S")
            print(f'Name: {name}, Type: {mime_type}, Last Modified: {formatted_time}')

