import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from authenticator import authenticate
from datetime import datetime

service = authenticate()

# 2. List Files in the user's google drive
def listFiles():
    results = service.files().list(
        fields= "files(name, mimeType, modifiedTime)"
    ).execute()
    items = results.get('files', [])
    print(items)
    if not items:
        print('No files found')
    else:
        print('Files:')
        for item in items:
            print(item)
            # folder_id = item['id']
            name = item['name']
            mime_type = item['mimeType']
            modified_time = datetime.strptime(item['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_time = modified_time.strftime("%Y-%m-%dT%H:%M:%S")
            print(f'Name: {name}, Type: {mime_type}, Last Modified: {formatted_time}')

# 3. Select a file, upload it to the user's google drive
def selectFile():
    Tk().withdraw()
    file_path = askopenfilename()
    print(file_path)
    return file_path

def uploadFile(file_path, mime_type = None, folder_id = None):
    file_name = os.path.basename(file_path)

    file_metadata = {
        'name': file_name
    }

    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id,name'
    ).execute()

    print(f"File '{file.get('name')}' uploaded successfully with file ID: {file.get('id')}")






