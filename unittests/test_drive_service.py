import unittest
from unittest.mock import patch, MagicMock
from drive_service import DriveService
import os
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class TestDriveService(unittest.TestCase):

    def setUp(self):
        # Mock the Google Drive API service
        self.mock_credentials = MagicMock()
        self.mock_service = MagicMock()

        # Mock the build function in googleapiclient.discovery
        with patch("googleapiclient.discovery.build", return_value=self.mock_service):
            self.service = DriveService(self.mock_credentials)

    def test_list_files(self):
        # Mock the return value of the list method
        self.mock_service.files.return_value.list.return_value.execute.return_value = {
            'files': [{'id': 'file_id_1', 'name': 'file1.txt', 'mimeType': 'text/plain',
                       'modifiedTime': '2024-01-01T00:00:00Z'}]
        }

        # Call the method to test
        files = self.service.list_files('folder_id')

        # Assert that the returned list of files matches the mocked value
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]['name'], 'file1.txt')

    def test_upload_file(self):
        # Mock the MediaFileUpload instance
        with patch("googleapiclient.http.MediaFileUpload") as mock_media_file_upload:
            mock_media_file_upload.return_value = MagicMock()

            # Mock the behavior of the create method
            self.mock_service.files.return_value.create.return_value.execute.return_value = {}

            # Call the upload_file method
            self.service.upload_file('test.txt', 'folder_id')

            # Assert that the files.create method was called once
            self.mock_service.files().create.assert_called_once()

            # Assert that MediaFileUpload was called with the correct parameters
            mock_media_file_upload.assert_called_once_with('test.txt')

    def test_delete_file(self):
        # Mock the delete method
        self.mock_service.files.return_value.delete.return_value.execute.return_value = {}

        # Call the delete_file method
        self.service.delete_file('file_id')

        # Assert that the delete method was called with the correct file_id
        self.mock_service.files().delete.assert_called_once_with(fileId='file_id')

    @patch("io.FileIO")
    @patch("googleapiclient.http.MediaIoBaseDownload")
    def test_download_file(self, mock_media_io_base_download, mock_file_io):
        # Mock the download request
        mock_request = MagicMock()
        self.mock_service.files.return_value.get_media.return_value = mock_request

        # Mock the MediaIoBaseDownload instance
        mock_downloader = MagicMock()
        mock_media_io_base_download.return_value = mock_downloader
        mock_downloader.next_chunk.side_effect = [(None, False), (None, True)]  # Simulate download chunks

        # Call the download_file method
        self.service.download_file('file_id', 'downloaded_file.txt')

        # Assert that the file was opened correctly
        mock_file_io.assert_called_once_with('downloaded_file.txt', 'wb')

        # Assert that the request was made with the correct file_id
        self.mock_service.files().get_media.assert_called_once_with(fileId='file_id')


if __name__ == '__main__':
    unittest.main()
