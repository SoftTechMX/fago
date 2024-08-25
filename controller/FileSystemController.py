# FileSystemController
# 
# Este controlador se encarga de gestionar tareas comunes con el sistema de ficheros.

import os

class FileSystemController:

    def get_home_directory(self):
        return os.path.expanduser("~")
    
    """_summary_

    Args:
        ruta (String): La ruta de donde se desea consultar los directorios

    Returns:
        _type_: Una lista con los nombres de los directorios
    """
    def get_directories(self, ruta):
        nodos = os.listdir(ruta)
        carpetas = []

        for nodo in nodos:
            ruta_completa = os.path.join(ruta, nodo)

            if os.path.isdir(ruta_completa):
                carpetas.append(nodo)
        
        return carpetas

    """_summary_

    Args:
        ruta (_type_): _description_

    Returns:
        _type_: _description_
    """
    def get_files(self, ruta):
        nodos = os.listdir(ruta)
        carpetas = []

        for nodo in nodos:
            ruta_completa = os.path.join(ruta, nodo)

            if os.path.isfile(ruta_completa):
                carpetas.append(nodo)
        
        return carpetas