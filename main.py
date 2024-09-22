import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from authenticator import authenticate
from drive_operations import listFiles, selectFile, uploadFile

service = authenticate()

listFiles()
file = selectFile()
folder_id = input("Enter the Google Drive folder ID (Leave blank to upload to root directory)")

if file:
    uploadFile(file, folder_id if folder_id else None)
else:
    print("No file selected.")