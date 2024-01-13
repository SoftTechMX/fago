import os

class FileSystemController:
    def get_home(self):
        return os.path.expanduser("~")
