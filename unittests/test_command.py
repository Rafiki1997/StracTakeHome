import unittest
from unittest.mock import MagicMock
from command import UploadCommand, DeleteCommand


class TestUploadCommand(unittest.TestCase):

    def test_upload_execute(self):
        mock_drive_service = MagicMock()
        command = UploadCommand(mock_drive_service, 'test_file.txt', 'folder_id')
        command.execute()
        mock_drive_service.upload_file.assert_called_once_with('test_file.txt', 'folder_id')


class TestDeleteCommand(unittest.TestCase):

    def test_delete_execute(self):
        mock_drive_service = MagicMock()
        command = DeleteCommand(mock_drive_service, 'file_id')
        command.execute()
        mock_drive_service.delete_file.assert_called_once_with('file_id')


if __name__ == '__main__':
    unittest.main()
