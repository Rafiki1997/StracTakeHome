import tkinter as tk
from tkinter import messagebox, filedialog
from command import UploadCommand, DeleteCommand
from datetime import datetime

class FileManagerGUI:
    def __init__(self, drive_service):
        self.drive_service = drive_service
        self.current_folder_id = None  # This should be set to 'root' initially
        self.folder_stack = []
        self.listbox = None

    def create_gui(self):
        root = tk.Tk()
        root.title("Google Drive File Manager")

        self.listbox = tk.Listbox(root, height=30, width=80)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        button_frame = tk.Frame(root)
        button_frame.pack(side="top", fill="x")

        delete_button = tk.Button(button_frame, text="Delete File", command=self.on_delete)
        delete_button.pack(side="left")

        download_button = tk.Button(button_frame, text="Download File", command=self.on_download)
        download_button.pack(side="left")

        upload_button = tk.Button(button_frame, text="Upload File", command=self.on_upload)
        upload_button.pack(side="left")

        open_folder_button = tk.Button(button_frame, text="Open Folder", command=self.on_open_folder)
        open_folder_button.pack(side="left")

        back_button = tk.Button(button_frame, text="Go Back", command=self.on_go_back)
        back_button.pack(side="left")

        self.update_file_list()  # Initialize the file list
        root.mainloop()

    def update_file_list(self):
        self.listbox.delete(0, 'end')  # Clear current list
        files = self.drive_service.list_files(self.current_folder_id)
        for file in files:
            modified_time = datetime.strptime(file['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_time = modified_time.strftime("%Y-%m-%d %H:%M:%S")
            display_text = f"{file['name']} (Type: {file['mimeType']}, Last Modified: {formatted_time})"
            self.listbox.insert("end", display_text)

    def on_delete(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            file_index = selected_index[0]
            selected_file = self.drive_service.list_files(self.current_folder_id)[file_index]
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_file['name']}'?")
            if confirm:
                command = DeleteCommand(self.drive_service, selected_file['id'])
                command.execute()
                self.update_file_list()

    def on_download(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            file_index = selected_index[0]
            selected_file = self.drive_service.list_files(self.current_folder_id)[file_index]
            save_path = filedialog.asksaveasfilename(defaultextension="*.*", title="Select Download Location", initialfile=selected_file['name'])
            if save_path:
                self.drive_service.download_file(selected_file['id'], save_path)

    def on_upload(self):
        file_path = filedialog.askopenfilename(title="Select a file to upload")
        if file_path:
            command = UploadCommand(self.drive_service, file_path, self.current_folder_id)
            command.execute()
            self.update_file_list()

    def on_open_folder(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            file_index = selected_index[0]
            selected_file = self.drive_service.list_files(self.current_folder_id)[file_index]
            if selected_file['mimeType'] == 'application/vnd.google-apps.folder':
                # Push the current folder ID onto the stack before changing it
                self.folder_stack.append(self.current_folder_id)
                self.current_folder_id = selected_file['id']
                self.update_file_list()

    def on_go_back(self):
        if self.folder_stack:
            self.current_folder_id = self.folder_stack.pop()  # Get the last folder ID from the stack
            self.update_file_list()
        else:
            messagebox.showinfo("Info", "You are already at the root folder.")

