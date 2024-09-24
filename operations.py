import os
import io
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    # Authenticate User and return service instance
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def listFiles(service, folder_id=None):
    #List files in root directory if folder ID isnt provided
    query = f"'{folder_id}' in parents" if folder_id else "'root' in parents"
    results = service.files().list(q=query, fields="files(id, name, mimeType, modifiedTime)").execute()
    return results.get('files', [])

def listFolders(service):
    #List all folder in the users google drive
    results = service.files().list(q="mimeType='application/vnd.google-apps.folder'", fields="files(id, name)").execute()
    return results.get('files', [])

def deleteFile(service, file_id):
    #Delete a file from the user's google drive based off file id
    service.files().delete(fileId=file_id).execute()

def downloadFile(service, file_id, save_path):
    #Download file from user's google drive based off file id
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(save_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

def uploadFile(service, file_path, folder_id=None):
    #Upload file to the user's google drive
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path)
    service.files().create(body=file_metadata, media_body=media).execute()

def updateFileList(service, listbox, folder_id=None):
    #Update listbox with files from the user's google drive
    listbox.delete(0, 'end')  # Clear the current list
    files = listFiles(service, folder_id)
    for file in files:
        modified_time = datetime.strptime(file['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_time = modified_time.strftime("%Y-%m-%d %H:%M:%S")
        display_text = f"{file['name']} (Type: {file['mimeType']}, Last Modified: {formatted_time})"
        listbox.insert("end", display_text)
    return files

def onDelete(service, listbox, folder_id):
    #Delete the file from the user's google drive
    selected_index = listbox.curselection()
    if selected_index:
        file_index = selected_index[0]
        selected_file = listFiles(service, folder_id)[file_index]
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{selected_file['name']}'?")
        if confirm:
            deleteFile(service, selected_file['id'])
            updateFileList(service, listbox, folder_id)

def onDownload(service, listbox, folder_id):
    #Download a file from the user's google drive
    selected_index = listbox.curselection()
    if selected_index:
        file_index = selected_index[0]
        selected_file = listFiles(service, folder_id)[file_index]  # Use folder_id to fetch the correct file
        save_path = filedialog.asksaveasfilename(defaultextension="*.*", title="Select Download Location", initialfile=selected_file['name'])
        if save_path:
            downloadFile(service, selected_file['id'], save_path)

def onUpload(service, folder_id, listbox):
    #Upload a file to the user's google drive
    file_path = filedialog.askopenfilename(title="Select a file to upload")
    if file_path:
        uploadFile(service, file_path, folder_id)
        updateFileList(service, listbox, folder_id)

def onOpenFolder(service, listbox, folder_id, folder_stack):
    #Open folders
    selected_index = listbox.curselection()
    if selected_index:
        file_index = selected_index[0]
        selected_file = listFiles(service, folder_id)[file_index]
        if selected_file['mimeType'] == 'application/vnd.google-apps.folder':
            new_folder_id = selected_file['id']
            folder_stack.append(folder_id)  # Push current folder onto the stack
            updateFileList(service, listbox, new_folder_id)
            return new_folder_id
    return folder_id

def onGoBack(service, listbox, folder_stack):
    #Return to parent folder
    if folder_stack:
        parent_folder_id = folder_stack.pop()  # Pop the last folder ID from the stack
        updateFileList(service, listbox, parent_folder_id)
        return parent_folder_id
    return None  # If no parent folder, stay at root

def createGUI(service):
    # Create Application Window
    root = tk.Tk()
    root.title("Google Drive File Manager")

    listbox = tk.Listbox(root, height=30, width=80)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    button_frame = tk.Frame(root)
    button_frame.pack(side="top", fill="x")

    # Store current folder ID and folder stack
    current_folder_id = None
    folder_stack = []

    def update_current_folder_id(new_folder_id):
        """Update the current folder ID."""
        nonlocal current_folder_id
        current_folder_id = new_folder_id

    delete_button = tk.Button(button_frame, text="Delete File", command=lambda: onDelete(service, listbox, current_folder_id))
    delete_button.pack(side="left")

    download_button = tk.Button(button_frame, text="Download File", command=lambda: onDownload(service, listbox, current_folder_id))
    download_button.pack(side="left")

    upload_button = tk.Button(button_frame, text="Upload File", command=lambda: onUpload(service, current_folder_id, listbox))
    upload_button.pack(side="left")

    open_folder_button = tk.Button(button_frame, text="Open Folder", command=lambda:
        update_current_folder_id(onOpenFolder(service, listbox, current_folder_id, folder_stack)))
    open_folder_button.pack(side="left")

    back_button = tk.Button(button_frame, text="Go Back", command=lambda:
        update_current_folder_id(onGoBack(service, listbox, folder_stack)))
    back_button.pack(side="left")

    # Initialize the file list
    updateFileList(service, listbox)

    root.mainloop()

