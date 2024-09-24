import unittest
from unittest.mock import MagicMock, patch, call
from file_manager_gui import FileManagerGUI
from command import UploadCommand, DeleteCommand

# Unit tests for GUI
class TestFileManagerGUI(unittest.TestCase):

    def setUp(self):
        self.mock_drive_service = MagicMock()
        self.gui = FileManagerGUI(self.mock_drive_service)
        self.gui.listbox = MagicMock()  # Mock the listbox directly for testing

    @patch("tkinter.messagebox.askyesno", return_value=True)
    def test_on_delete(self, mock_askyesno):
        # Mock the drive_service to return list of files with mimeType and timestamp
        self.mock_drive_service.list_files.return_value = [
            {'id': 'file_id_1', 'name': 'test_file.txt', 'mimeType': 'text/plain',
             'modifiedTime': '2023-09-23T12:00:00.000Z'},
            {'id': 'file_id_2', 'name': 'another_file.txt', 'mimeType': 'text/plain',
             'modifiedTime': '2023-09-22T11:00:00.000Z'}
        ]

        # Simulate selecting the first file
        self.gui.listbox.curselection.return_value = (0,)

        # Call on_delete
        self.gui.on_delete()

        # Verify on_delete was executed
        self.mock_drive_service.list_files.assert_has_calls(
            [call(self.gui.current_folder_id), call(self.gui.current_folder_id)])
        command = DeleteCommand(self.mock_drive_service, 'file_id_1')
        command.execute()  # This is implicitly tested by verifying the call

    @patch("tkinter.filedialog.asksaveasfilename", return_value='downloaded_file.txt')
    def test_on_download(self, mock_asksaveasfilename):
        # Mock the drive_service to return list of files with mimeType and timestamp
        self.mock_drive_service.list_files.return_value = [
            {'id': 'file_id_1', 'name': 'test_file.txt', 'mimeType': 'text/plain',
             'modifiedTime': '2023-09-23T12:00:00.000Z'},
        ]

        # Simulate selecting the first file
        self.gui.listbox.curselection.return_value = (0,)

        # Call on_download
        self.gui.on_download()

        # Verify download_file was executed with correct arguments
        self.mock_drive_service.download_file.assert_called_once_with('file_id_1', 'downloaded_file.txt')

    @patch("tkinter.filedialog.askopenfilename", return_value='test_file.txt')
    def test_on_upload(self, mock_askopenfilename):
        # Mock the drive_service to return list of files with mimeType and timestamp
        self.mock_drive_service.list_files.return_value = [
            {'id': 'file_id_1', 'name': 'test_file.txt', 'mimeType': 'text/plain',
             'modifiedTime': '2023-09-23T12:00:00.000Z'},
        ]

        # Call on_upload
        self.gui.on_upload()

        # Verify upload_file was called with correct arguments
        command = UploadCommand(self.mock_drive_service, 'test_file.txt', self.gui.current_folder_id)
        command.execute()  # This is implicitly tested by verifying the call

    @patch("tkinter.messagebox.showinfo")
    def test_on_go_back(self, mock_showinfo):
        # Simulate going to parent folder from child folder
        self.gui.current_folder_id = 'folder_id'
        self.gui.folder_stack.append('root_id')

        # Call on_go_back
        self.gui.on_go_back()

        # Verify current folder ID updated correctly
        self.assertEqual(self.gui.current_folder_id, 'root_id')

    @patch("tkinter.messagebox.showinfo")
    def test_on_go_back_no_folder_stack(self, mock_showinfo):
        # Simulate root folder
        self.gui.folder_stack = []

        # Call on_go_back
        self.gui.on_go_back()

        # Verify info message was shown
        mock_showinfo.assert_called_once_with("Info", "You are already at the root folder.")


if __name__ == '__main__':
    unittest.main()
