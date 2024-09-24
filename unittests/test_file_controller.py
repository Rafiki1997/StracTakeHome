import unittest
from unittest.mock import MagicMock
from file_controller import FileController  # Adjust based on your actual file structure


class TestFileController(unittest.TestCase):

    def setUp(self):
        self.mock_drive_service = MagicMock()  # Mocking the drive service
        self.mock_gui = MagicMock()  # Mocking the GUI
        self.controller = FileController(self.mock_drive_service, self.mock_gui)

    def test_handle_upload(self):
        # Call the handle_upload method
        self.controller.handle_upload()

        # Verify that the on_upload method of the GUI was called once
        self.mock_gui.on_upload.assert_called_once()

    def test_handle_delete(self):
        # Call the handle_delete method
        self.controller.handle_delete()

        # Verify that the on_delete method of the GUI was called once
        self.mock_gui.on_delete.assert_called_once()

    def test_handle_download(self):
        # Call the handle_download method
        self.controller.handle_download()

        # Verify that the on_download method of the GUI was called once
        self.mock_gui.on_download.assert_called_once()


if __name__ == '__main__':
    unittest.main()
