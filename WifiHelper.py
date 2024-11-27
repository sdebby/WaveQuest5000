import subprocess
import requests

class WifiHelper:

    def CheckCunectivity():
        """
        Check internet conectivity\n
        Return True if connection avalable.
        """
        url='http://www.google.com/'
        timeout=5
        try:
            response = requests.get(url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    
    def ConnectWifi(SSID:str,Pass:str):
        """
        Linux\n
        Connecting to new network\n
        - SSID - New network SSID\n
        - Pass - New network password
        """
        command = f'nmcli device wifi connect "{SSID}" password "{Pass}"'
        subprocess.run(command, shell=True)
        print(f"Connected to {SSID}")

    def WifiDisable():
        """
        Linux\n
        Disabeling wifi connection
        """
        subprocess.run('nmcli radio wifi off', shell=True)
        print("Wi-Fi disabled")

    def WifiEnable():
        """
        Linux\n
        Enabeling wifi connection
        """
        subprocess.run('nmcli radio wifi on', shell=True)
        print("Wi-Fi enabled")