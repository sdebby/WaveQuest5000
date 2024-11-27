# 30.05.24
# WaveQuest5000 project
# mobile vision-voice chat device using Pi Zero

import glob
import os, argparse, sys
import threading
from gpiozero import Button, LED
import sounddevice as sd
import numpy as np
import queue
import time
import SoundHelper as SH
from OpenAIHelper import OpenAIHelper as AIH
from CameraHelper import CameraHelper as CamH
from WifiHelper import WifiHelper as WiFiH
from USDdeviceHelper import USDDevHelper as USDDev


# Chat parameters
max_tok=750
temp=0.7
ChatModel="gpt-4o-mini"
msglist=[]
ChatRole='Act as a friend, reply only by simple text'
AIvoice = ['alloy','echo','fable','onyx','nova','shimmer']
SelectAIvoice = AIvoice[4]
dev_index = 0

# Recording parameters
sample_rate = 48000
Channels=1
dtype = 'int16'
audio_queue = queue.Queue() # Define a queue to communicate between the recording thread and main thread
dev_index = 1
BlockSize=1024
led = LED(18)
BtnSpk = Button(23,hold_time=1)
BtnSCam = Button(24)
RFlag = False
CamFlag = False # Camera flag if picture taken
filenameImg = "" # image name

# Delete all files in a folder
def CleanFiles(FileSet:str):
    print('deleting files ',FileSet)
    files = glob.glob(FileSet, recursive=True)
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

def ImgBtnThread():
    print('Registering image button thread')
    BtnSCam.when_pressed = imgCapture
    BtnSCam.when_released = on_button_released

def on_button_released():
    print('Button released')

# Function to record audio
def record_audio():
    audio_data = np.array([], dtype=dtype)
    def callback(indata, frames, time, status):
        global RFlag
        if status:
            print(status)
        # Put the incoming data into the queue
        if RFlag:
            audio_queue.put(indata.copy())
                
    # Start the stream
    with sd.InputStream(samplerate=sample_rate, blocksize=BlockSize, channels=Channels, device=dev_index, callback=callback):
        global RFlag
        while True:
            BtnSpk.wait_for_press()
            led.on()
            RFlag = True
            print("Recording...")
            while True:
                audio_data = np.append(audio_data, audio_queue.get())
                if not BtnSpk.is_pressed:  
                    time.sleep(1)
                    RFlag = False
                    break

            led.off()
            print("Recording stopped.")        
            audio_data =SH.RecHelper. normalize_audio(audio_data, dtype) # Normalize the recording
            filenameWAV = f"recording_{int(time.time())}.wav"
            SH.RecHelper.save_to_file(audio_data, dtype, sample_rate,filenameWAV) # Save the recording to a file
            audio_data = np.array([], dtype=dtype)
            
            UserTranslation=AIH.STT(filenameWAV).text # transcript to text

            if not UserTranslation == 'err': # if not error code continue       
                msg1={"role": "user", "content": UserTranslation}
                msglist.append(msg1) # adding user message to list
                global CamFlag
                global filenameImg
                if CamFlag:
                    # Picture taken
                    CamFlag = False # reset flag
                    Base64IMG = AIH.EncodeImage(filenameImg)
                    ChatResponce = AIH.ImageResponse(Base64IMG,ChatModel,300,UserTranslation) #sending image + user meassage to chat

                else:
                    # No picture taken
                    ChatResponce = AIH.Chat(ChatModel,temp,max_tok,msglist) #sending message list to chat

                msg2={"role": "assistant", "content": ChatResponce} # Add responce to list
                msglist.append(msg2)

                # filenameWAVResponse=filenameWAV.split('.')[0]+'+ConvWAV.wav'
                # AIH.TTS(ChatResponce,filenameWAVResponse,SelectAIvoice) # convert text to speach
                # SH.PlayHelper.PlayWAVToUSB(filenameWAVResponse,dev_index) #play to USB device

                # AIH.TTSStream(ChatResponce,SelectAIvoice) # Stream voice response
                resWords = len(ChatResponce.split())
                AIH.TTSStreamConvert(ChatResponce,SelectAIvoice,resWords * 1024 * 20) # Stream voice response while converting sample rate (for Raspberry pi USB output)

# Function to capture image
def imgCapture():
    print('Capturing image')
    global filenameImg
    filenameImg = f"recording_{int(time.time())}.jpg"
    CamH.Cature(filenameImg)
    global CamFlag
    CamFlag = True
    SH.PlayHelper.PlayWAVToUSB('media/camSound.wav',dev_index) #play to USB device
    
def main():
    CleanFiles('*.wav')
    CleanFiles('*.mp3')
    CleanFiles('*.jpg')
    print("Checking USD devices")
    if not USDDev.IsDeviceConnected("Y02"): # Check if USB sound device is connected, if not - exit script
        print('No USB sound/mic device - exiting script')
        sys.exit()
    print("Checking internet connection")
    if not WiFiH.CheckCunectivity():
        print('No internet connection- exiting script')
        SH.PlayHelper.PlayWAVToUSB('media/noWIFI.wav',dev_index) #play no wifi recording
        sys.exit()
    else:
        print('Found internet connection')
        print('--- Starting ---')
        SH.PlayHelper.PlayWAVToUSB('media/WelcomeIntro.wav',dev_index) #play welcome
        msglist.append({"role": "system", "content": ChatRole})
        # Run the record_audio function in a separate thread
        threading.Thread(target=record_audio).start()
        threading.Thread(target=ImgBtnThread).start()

if __name__ == '__main__':
    main()