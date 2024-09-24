class FileController:
    def __init__(self, drive_service, gui):
        self.drive_service = drive_service
        self.gui = gui

    def handle_upload(self):
        self.gui.on_upload()

    def handle_delete(self):
        self.gui.on_delete()

    def handle_download(self):
        self.gui.on_download()
