# command.py
class Command:
    def execute(self):
        pass

# Method to upload file from google drive
class UploadCommand(Command):
    # Intialize parameters for upload
    def __init__(self, drive_service, file_path, folder_id):
        self.drive_service = drive_service
        self.file_path = file_path
        self.folder_id = folder_id

    # Call drive_service upload file method
    def execute(self):
        self.drive_service.upload_file(self.file_path, self.folder_id)

# Method to delete file from google drive
class DeleteCommand(Command):
    # Initialize parameters for delete
    def __init__(self, drive_service, file_id):
        self.drive_service = drive_service
        self.file_id = file_id
    # Call drive_service delete method
    def execute(self):
        self.drive_service.delete_file(self.file_id)
