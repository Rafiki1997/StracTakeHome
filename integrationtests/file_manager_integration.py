from main import AuthServiceFactory, DriveService, FileManagerGUI, FileController
import os
# Note: This is incomplete due to time limitations.

def test_main_integration(self):
    target_file = "README.md"
    drive_service = None
    # Read target file, save its contents
    with open(target_file, "r") as f:
        file_contents = f.read()

    # Authenticate
    auth_service = AuthServiceFactory.create_auth_service()
    credentials = auth_service.authenticate()

    if credentials:
        drive_service = DriveService(credentials)

    assert drive_service is not None

    # Upload a file
    fake_gui = FileManagerGUI(drive_service)
    fake_gui.on_upload(target_file)

    # List Files (check if our file is there)
    file_list = fake_gui.update_file_list()
    file_names = []
    for file in file_list:
        file_names.append(file['name'])
    assert target_file in file_names

    # Download the file
    fake_gui.on_download(os.getcwd() + "target_file_download")

    # Read the file, check its contents
    # Unfortunately, I ran out of time and could not fill this out.

if __name__ == "__main__":
    test_main_integration()
