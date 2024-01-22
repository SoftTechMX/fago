import sqlite3
import os
from controller.FileSystemController    import FileSystemController

# \AppData\Local\Google\Chrome\User Data\Default\Cache
class GoogleChromeController:
    
    def __init__(self):
        self.fs_controller = FileSystemController()
        self.db_directory = self.fs_controller.get_home_directory() + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\'

    def get_download_history(self):
        # target_path
        # start_time
        # tab_url sino referrer
        db_file = self.db_directory + 'History'

        if os.path.exists(db_file):
            try:
                conexion = sqlite3.connect(db_file)
                cursor = conexion.cursor()
                cursor.execute('SELECT * FROM downloads')
                filas = cursor.fetchall()
                nombres_columnas = [descripcion[0] for descripcion in cursor.description]
                array_de_diccionarios = []

                for fila in filas:
                    diccionario_fila = dict(zip(nombres_columnas, fila))
                    array_de_diccionarios.append(diccionario_fila)

                return array_de_diccionarios

            except Exception as exception:
                print(f"Ocurrió una excepción: {exception}")
                return None
        else:
            print("NO EXISTE")
            return None