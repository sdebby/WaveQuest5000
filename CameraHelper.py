from picamera2 import Picamera2
import time

class CameraHelper:
    def Cature(inFile:str):
        """
        Capture image\n
        - inFile : File name to save image in jpg format
        """
        try:
            picam2 = Picamera2()
            config = picam2.create_still_configuration(main={"size": (3280 , 2464)})
            picam2.configure(config)
            picam2.start()
            time.sleep(1)
            picam2.capture_file(inFile)
            picam2.stop()
            picam2.close()
            print("Image captured successfully!")
        except Exception as e:
            print(f"An error occurred with the capturing image: {e}")