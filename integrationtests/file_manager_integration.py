import unittest
from unittest.mock import patch, MagicMock
from main import AuthServiceFactory, DriveService, FileManagerGUI, FileController


class TestFileManagerIntegration(unittest.TestCase):

    @patch('main.FileManagerGUI.create_gui')  # Patch the GUI creation
    @patch('main.DriveService')  # Patch where DriveService is used in main.py
    @patch('main.auth_service.AuthService.authenticate')  # Patch where auth_service.AuthService is used in main.py
    def test_main_integration(self, mock_authenticate, mock_drive_service, mock_create_gui):
        # Mocking Authentication
        mock_authenticate.return_value = MagicMock()  # Simulates valid credentials

        # Mocking DriveService instance
        mock_drive_service_instance = MagicMock()
        mock_drive_service.return_value = mock_drive_service_instance

        # Run your logic from the main.py file (this simulates running the application)
        auth_service = AuthServiceFactory.create_auth_service()
        credentials = auth_service.authenticate()

        self.assertIsNotNone(credentials)  # Ensure credentials were retrieved

        drive_service = DriveService(credentials)

        # Mocking file operations
        drive_service.upload_file = MagicMock()
        drive_service.download_file = MagicMock()
        drive_service.delete_file = MagicMock()

        # Test the FileManagerGUI initialization
        gui = FileManagerGUI(drive_service)
        controller = FileController(drive_service, gui)

        gui.create_gui()  # Simulate the GUI creation

        # Assertions to check that components interacted as expected
        mock_create_gui.assert_called_once()  # Check if GUI creation was called
        mock_drive_service.assert_called_once_with(credentials)  # Check if DriveService was called with credentials

        # Simulating file operations
        drive_service.upload_file('test.txt', 'folder_id')
        drive_service.download_file('file_id', 'downloaded.txt')
        drive_service.delete_file('file_id')

        # Check file operations were called
        drive_service.upload_file.assert_called_once_with('test.txt', 'folder_id')
        drive_service.download_file.assert_called_once_with('file_id', 'downloaded.txt')
        drive_service.delete_file.assert_called_once_with('file_id')


if __name__ == "__main__":
    unittest.main()
