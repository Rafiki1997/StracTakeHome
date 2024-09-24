import os
import io
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build

class DriveService:
    # Initialize google drive service instance
    def __init__(self, credentials):
        self.service = build('drive', 'v3', credentials=credentials)

    # List files in user's google drive
    def list_files(self, folder_id=None):
        query = f"'{folder_id}' in parents" if folder_id else "'root' in parents"
        results = self.service.files().list(q=query, fields="files(id, name, mimeType, modifiedTime)").execute()
        return results.get('files', [])

    # Upload file from local file system to user's google drive
    def upload_file(self, file_path, folder_id=None):
        file_name = os.path.basename(file_path)
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(file_path)
        self.service.files().create(body=file_metadata, media_body=media).execute()

    # Delete file from user's google drive
    def delete_file(self, file_id):
        self.service.files().delete(fileId=file_id).execute()

    # Download file from user's google drive to local file system
    def download_file(self, file_id, save_path):
        request = self.service.files().get_media(fileId=file_id)
        with io.FileIO(save_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
