import os
import sqlite3

class SQLiteController:
    def __init__(self):
        pass

    def executeQuery(self, sql, db_path):
        if os.path.exists(db_path):
            try:
                conexion = sqlite3.connect(db_path)
                cursor = conexion.cursor()
                cursor.execute(sql)
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
    
    def truncate(self, table):
        pass