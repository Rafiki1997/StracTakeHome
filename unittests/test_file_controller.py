import unittest
from unittest.mock import MagicMock
from file_controller import FileController  # Adjust based on your actual file structure

# Unit tests for file_controller
class TestFileController(unittest.TestCase):
    # Mock drive service, gui, file controller
    def setUp(self):
        self.mock_drive_service = MagicMock()
        self.mock_gui = MagicMock()
        self.controller = FileController(self.mock_drive_service, self.mock_gui)

    def test_handle_upload(self):
        # Call handle_upload
        self.controller.handle_upload()

        # Verify that the on_upload was called once
        self.mock_gui.on_upload.assert_called_once()

    def test_handle_delete(self):
        # Call handle_delete
        self.controller.handle_delete()

        # Verify that on_delete was called once
        self.mock_gui.on_delete.assert_called_once()

    def test_handle_download(self):
        # Call handle_download
        self.controller.handle_download()

        # Verify on_download was called once
        self.mock_gui.on_download.assert_called_once()


if __name__ == '__main__':
    unittest.main()
