import unittest
from unittest.mock import patch, MagicMock
from drive_service import DriveService
import os
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# Unit tests for drive_service
# TODO: Look into unit testing GUI. Make this test functional. Time restrictions prevented me from finishing.
class TestDriveService(unittest.TestCase):

    def setUp(self):
        # Mock Google drive API service + Credentials
        self.mock_credentials = MagicMock()
        self.mock_service = MagicMock()

        # Mock googleapiclient build method to return mocked service
        # Allows tests to run without real google drive API
        with patch("googleapiclient.discovery.build", return_value=self.mock_service):
            self.service = DriveService(self.mock_credentials)

    # Verify driveservice list_files returns expected list from google drive API
    def test_list_files(self):
        self.mock_service.files.return_value.list.return_value.execute.return_value = {
            'files': [{'id': 'file_id_1', 'name': 'file1.txt', 'mimeType': 'text/plain',
                       'modifiedTime': '2024-01-01T00:00:00Z'}]
        }

        files = self.service.list_files('folder_id')

        # Verify return values and mocked values match
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]['name'], 'file1.txt')

    # Simulate upload_file without actually uploading a file
    def test_upload_file(self):
        # Mock MediaFileUpload
        with patch("googleapiclient.http.MediaFileUpload") as mock_media_file_upload:
            mock_media_file_upload.return_value = MagicMock()

            # Mock google drive file creation method
            self.mock_service.files.return_value.create.return_value.execute.return_value = {}

            # Call the upload_file method
            self.service.upload_file('test.txt', 'folder_id')

            # Verify create was called once
            self.mock_service.files().create.assert_called_once()

            # Verify file name is correct
            mock_media_file_upload.assert_called_once_with('test.txt')

    def test_delete_file(self):
        # Mock the delete method of google API service
        self.mock_service.files.return_value.delete.return_value.execute.return_value = {}

        # Call the delete_file method
        self.service.delete_file('file_id')

        # Verify delete was called with correct file ID
        self.mock_service.files().delete.assert_called_once_with(fileId='file_id')

    @patch("io.FileIO")
    @patch("googleapiclient.http.MediaIoBaseDownload")
    def test_download_file(self, mock_media_io_base_download, mock_file_io):
        # Mock the download request
        mock_request = MagicMock()
        self.mock_service.files.return_value.get_media.return_value = mock_request

        # Mock the google drive mediadownload object
        mock_downloader = MagicMock()
        mock_media_io_base_download.return_value = mock_downloader
        mock_downloader.next_chunk.side_effect = [(None, False), (None, True)]  # Simulate download chunks

        # Call download_file from service
        self.service.download_file('file_id', 'downloaded_file.txt')

        # Verify file was opened correctly
        mock_file_io.assert_called_once_with('downloaded_file.txt', 'wb')

        # Verify correct file ID was called
        self.mock_service.files().get_media.assert_called_once_with(fileId='file_id')


if __name__ == '__main__':
    unittest.main()
