# FileSystemController
# 
# Este controlador se encarga de gestionar tareas comunes con el sistema de ficheros.

import os

class FileSystemController:
    def get_home(self):
        return os.path.expanduser("~")
