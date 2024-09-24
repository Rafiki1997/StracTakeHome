class FileController:
    # Controller to separate logic from controller and google drive service
    def __init__(self, drive_service, gui):
        self.drive_service = drive_service
        self.gui = gui
    # Call on_upload from GUI
    def handle_upload(self):
        self.gui.on_upload()
    # Call on_delete from GUI
    def handle_delete(self):
        self.gui.on_delete()
    # Call on_download from GUI
    def handle_download(self):
        self.gui.on_download()
