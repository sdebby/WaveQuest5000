# Get USB devices helper
import subprocess

class USDDevHelper:

    def IsDeviceConnected(device_name:str):
        '''
        This helper will check if USB device is connected
        Works on Linux
        '''
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True, check=True)
            # Check if the specified device name is in the output
            if device_name in result.stdout:
                print(f"Device '{device_name}' is connected.")
                return True
            else:
                print(f"Device '{device_name}' is not connected.")
                return False

        except subprocess.CalledProcessError as e:
            print("An error occurred while trying to list USB devices.")
            print(e)
    
    def ListDevices():
        '''
        List Connected USB devices
        Works on Linux
        '''
        try:
            # Run the 'lsusb' command to list USB devices
            result = subprocess.run(['lsusb'], capture_output=True, text=True, check=True)
            # Output the result
            print("USB Devices:")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print("An error occurred while trying to list USB devices.")
            print(e)