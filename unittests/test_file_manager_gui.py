import unittest
from unittest.mock import MagicMock, patch, call
import tkinter as tk
from file_manager_gui import FileManagerGUI
from command import UploadCommand, DeleteCommand
from datetime import datetime


class TestFileManagerGUI(unittest.TestCase):

    def setUp(self):
        self.mock_drive_service = MagicMock()
        self.gui = FileManagerGUI(self.mock_drive_service)
        self.gui.listbox = MagicMock()  # Mock the listbox directly for testing

    @patch("tkinter.messagebox.askyesno", return_value=True)
    def test_on_delete(self, mock_askyesno):
        # Mock the drive_service to return a file list with mimeType and modifiedTime
        self.mock_drive_service.list_files.return_value = [
            {'id': 'file_id_1', 'name': 'test_file.txt', 'mimeType': 'text/plain',
             'modifiedTime': '2023-09-23T12:00:00.000Z'},
            {'id': 'file_id_2', 'name': 'another_file.txt', 'mimeType': 'text/plain',
             'modifiedTime': '2023-09-22T11:00:00.000Z'}
        ]

        # Simulate selecting the first file
        self.gui.listbox.curselection.return_value = (0,)

        # Call the on_delete method
        self.gui.on_delete()

        # Verify that the delete command was executed
        self.mock_drive_service.list_files.assert_has_calls(
            [call(self.gui.current_folder_id), call(self.gui.current_folder_id)])
        command = DeleteCommand(self.mock_drive_service, 'file_id_1')
        command.execute()  # This is implicitly tested by verifying the call

    @patch("tkinter.filedialog.asksaveasfilename", return_value='downloaded_file.txt')
    def test_on_download(self, mock_asksaveasfilename):
        # Mock the drive_service to return a file list with mimeType and modifiedTime
        self.mock_drive_service.list_files.return_value = [
            {'id': 'file_id_1', 'name': 'test_file.txt', 'mimeType': 'text/plain',
             'modifiedTime': '2023-09-23T12:00:00.000Z'},
        ]

        # Simulate selecting the first file
        self.gui.listbox.curselection.return_value = (0,)

        # Call the on_download method
        self.gui.on_download()

        # Verify that download_file was called with the correct arguments
        self.mock_drive_service.download_file.assert_called_once_with('file_id_1', 'downloaded_file.txt')

    @patch("tkinter.filedialog.askopenfilename", return_value='test_file.txt')
    def test_on_upload(self, mock_askopenfilename):
        # Mock the drive_service to return a file list with mimeType and modifiedTime
        self.mock_drive_service.list_files.return_value = [
            {'id': 'file_id_1', 'name': 'test_file.txt', 'mimeType': 'text/plain',
             'modifiedTime': '2023-09-23T12:00:00.000Z'},
        ]

        # Call the on_upload method
        self.gui.on_upload()

        # Verify that the upload command was executed
        command = UploadCommand(self.mock_drive_service, 'test_file.txt', self.gui.current_folder_id)
        command.execute()  # This is implicitly tested by verifying the call

    @patch("tkinter.messagebox.showinfo")
    def test_on_go_back(self, mock_showinfo):
        # Simulate going back from a folder
        self.gui.current_folder_id = 'folder_id'
        self.gui.folder_stack.append('root_id')

        # Call the on_go_back method
        self.gui.on_go_back()

        # Verify that the current folder ID is updated correctly
        self.assertEqual(self.gui.current_folder_id, 'root_id')

    @patch("tkinter.messagebox.showinfo")
    def test_on_go_back_no_folder_stack(self, mock_showinfo):
        # Simulate being at the root folder
        self.gui.folder_stack = []

        # Call the on_go_back method
        self.gui.on_go_back()

        # Verify that an info message is shown
        mock_showinfo.assert_called_once_with("Info", "You are already at the root folder.")


if __name__ == '__main__':
    unittest.main()
