from auth_service_factory import AuthServiceFactory
from drive_service import DriveService
from file_manager_gui import FileManagerGUI
from file_controller import FileController

if __name__ == "__main__":
    # Create Auth service and authenticate
    # If successful, instantiate drive service
    auth_service = AuthServiceFactory.create_auth_service()
    credentials = auth_service.authenticate()

    if credentials:
        drive_service = DriveService(credentials)

    # Create GUI from drive_service
    gui = FileManagerGUI(drive_service)
    controller = FileController(drive_service, gui)

    gui.create_gui()
