import configparser
import subprocess
import socket
import os
import re

from scapy.all                          import ARP, Ether, srp
from collections                        import namedtuple
from controller.LogController           import LogController

class NetworkController:
    
    def __init__(self):
        self.log = LogController()

    def get_wifi_ssids(self):
        output = subprocess.check_output("netsh wlan show profiles").decode('latin-1')
        ssids = []
        profiles = re.findall(r"All User Profile\s(.*)", output)
        for profile in profiles:

            # for each SSID, remove spaces and colon
            ssid = profile.strip().strip(":").strip()

            # add to the list
            ssids.append(ssid)

        profiles = re.findall(r"Perfil de todos los usuarios\s(.*)", output)
        for profile in profiles:

            # for each SSID, remove spaces and colon
            ssid = profile.strip().strip(":").strip()

            # add to the list
            ssids.append(ssid)            
        return ssids

    def get_wifi_passwords(self):
        ssids = self.get_wifi_ssids()
        Profile = namedtuple("Profile", ["ssid", "ciphers", "key"])
        profiles = []
        for ssid in ssids:
            ssid_details = subprocess.check_output(f"""netsh wlan show profile "{ssid}" key=clear""").decode('latin-1')

            ciphers = re.findall(r"Cipher\s(.*)", ssid_details)                 # get the ciphers
            ciphers = "/".join([c.strip().strip(":").strip() for c in ciphers]) # clear spaces and colon

            try:                                                                
                key = re.findall(r"Key Content\s(.*)", ssid_details)            # get the Wi-Fi password
                if not key:
                    key = re.findall(r"Contenido de la clave\s(.*)", ssid_details) # get the Wi-Fi password

                key = key[0].strip().strip(":").strip()                         # clear spaces and colon
            except IndexError:
                key = "None"
            profile = Profile(ssid=ssid, ciphers=ciphers, key=key)
            profiles.append(profile)
        return profiles

    # target_ip = "192.168.1.1/24"
    def get_wifi_clients(self, CIDR):
        try:
            arp = ARP(pdst=CIDR)                        # create ARP packet
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")      # create the Ether broadcast packet ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
            packet = ether/arp                          # stack them
            result = srp(packet, timeout=3)[0]
            clients = []                                # a list of clients, we will fill this in the upcoming loop
        except Exception as execption:
            self.log.error(execption)
            return None
        
        for sent, received in result:
            # for each response, append ip and mac address to `clients` list
            clients.append({'ip': received.psrc, 'mac': received.hwsrc})
        
        return clients

    def is_port_open(self, IP, PORT):
        s = socket.socket()
        try:
            s.connect((IP, PORT))           # tries to connect to host using that port
            s.settimeout(0.2)               # make timeout if you want it a little faster ( less accuracy )
        except:
            return False                    # cannot connect, port is closed
        else:
            return True                     # the connection was established, port is open!