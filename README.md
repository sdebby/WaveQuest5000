# Project WaveQuest5000

![INTRO PICTURE](https://github.com/sdebby/WaveQuest5000/blob/main/media/WaveQuest5000%203.jpeg?raw=true)

## Overview
- A fun project to play with some hardware and software using OpenAI tools and raspberry pi.
 
## MRD (Marketing requirement)
- Creating a Vision-Chat mobile device.
- The device is connected to OpenAI services: Chat,vision and Whisperer (voice output).
- The device will be small and mobile.

## Equipment:
1. [Raspbbery pi zero 2 W.](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
2. SD card.
3. [Speakers + Microphone on USB device.](https://www.aliexpress.com/item/1005005929228163.html?spm=a2g0o.order_list.order_list_main.152.24e518023DI1FQ)
4. Camera - Pi camera V2.
5. [Battery charger.](https://www.aliexpress.com/item/1005006403572331.html?spm=a2g0o.order_list.order_list_main.131.24e518023DI1FQ)
6. 18650  mAmp battery.
7. 2 X Switch button.
8. 2 X Resistors 330 Ohm.
9. 3D printed case.
10. M1.6 self tapping screws

## Schematics:
![schmatics](https://github.com/sdebby/WaveQuest5000/blob/main/media/WaveQuest5000_bb.jpg?raw=true)

## Installation:
- On fresh install run `WaveQuest5000Install.sh` script, this will update system and install all requirements . 
- The script will install the following libraries:
  - Python Libraries installed using PIP:
    -  playsound == 1.2.2
    -  pydub
    -  gpiozero
    -  sounddevice
    -  soundfile
    -  openai
    -  requests
  - Python Libraries installed using APT:
    - python3-numpy
    - libportaudio2
    - ffmpeg
    - python3-pyaudio
    - python3-picamera2 --no-install-recommends
- Add your OpenAI API key as an environment variable under `OpenAI_Key`

## Hardware assembly:
USB microphone and speaker
![USB mic and speaker](https://github.com/sdebby/WaveQuest5000/blob/main/media/IMG_8075.jpg?raw=true)
---
USB mic and speaker- disassembled
![USB mic and speaker- disassembled](https://github.com/sdebby/WaveQuest5000/blob/main/media/IMG_8077.jpg?raw=true)
---
Buttons and breadboard
![Buttons and breadboard](https://github.com/sdebby/WaveQuest5000/blob/main/media/IMG_8507.jpg?raw=true)
---
Assembly on 3D printed case
![Assembly on 3D printed case](https://github.com/sdebby/WaveQuest5000/blob/main/media/IMG_8529.jpg?raw=true)
---
Assembly on 3D printed case
![Assembly on 3D printed case](https://github.com/sdebby/WaveQuest5000/blob/main/media/IMG_8530.jpg?raw=true)
---
Assembly on 3D printed case
![Assembly on 3D printed case](https://github.com/sdebby/WaveQuest5000/blob/main/media/IMG_8531.jpg?raw=true)
---
Close case front
![Close case](https://github.com/sdebby/WaveQuest5000/blob/main/media/IMG_8532.jpg?raw=true)
---
Close case back
![Cose case](https://github.com/sdebby/WaveQuest5000/blob/main/media/IMG_8533.jpg?raw=true)

## Checking current
* On boot - 500 mA peak (average of 300 mA).
  * Boot time including loading all libraries is 30 sec.
* On taking picture 400 mA.
* On playing sound from USB speakers 300 mA.
* On system ideal 200 mA.
* Using 2200 mAh with average of 300 mAh will work for 7.3 hours.

## 3D case design
* using Fusion360
* 3D print using Ender 5 plus

![Isometric 1](https://github.com/sdebby/WaveQuest5000/blob/main/media/WaveQuest5000%20v2%20v9.png?raw=true)
---
![Isonetric 2](https://github.com/sdebby/WaveQuest5000/blob/main/media/WaveQuest5000%20v2%20v9%20iso2.jpg?raw=true)

* 3D files are in [here](https://github.com/sdebby/WaveQuest5000/tree/main/3D)

## Skill set
* Using hardware parts to assemble the project.
* Design and 3D print.
* Communicating with OpenAI services using API.
* Coding in python on Raspberry pi to communicate with USB device and buttons 

## Behind the scenes:
1. Script run on machine start.
2. Deleting old files (from previous runs) 
3. Validates USB mic and speaker are connected
   1. Exit if not connected
4. Validates internet
   1. plays a message if no internet and exit
5. play welcome sound
6. Register buttons in different threads

On pressing rec_audio button :
1. Record audio from mic and save it WAV format.
2. Send WAV file to OpenAI `whisper` module and get transcript.
3. Save transcript in conversation log
4. Check in user capture an image
   On capturing image :
   1. Encoding image to base64.
   2. Sending image and user transcript to OpenAI `ImageResponce` module and get answer.
   On not capturing image :
   1. Send transcript to OpenAI `ChatGPT o1-mini` module and get answer.
5. Save answer in conversation log.
6. Send answer to OpenAI `Speech to text` module and get voice answer.
7. Play message to user (using stream to reduce latency).

On pressing Take_pic button
1. Capture image from builtin camera and save it in jpg format.
2. Play sound to user.

## Video

[![](https://markdown-videos-api.jorgenkh.no/youtube/Zx07er9c_9g)](https://youtu.be/Zx07er9c_9g)

## R&D
[link](https://platform.openai.com/docs/guides/vision)

`The Chat Completions API, unlike the Assistants API, is not stateful. That means you have to manage the messages (including images) you pass to the model yourself. If you want to pass the same image to the model multiple times, you will have to pass the image each time you make a request to the API.`

`For long running conversations, we suggest passing images via URL's instead of base64. The latency of the model can also be improved by downsizing your images ahead of time to be less than the maximum size they are expected them to be. `


* There is a option to run whisperer (Speech to text) on premiss (on device) without sending audio file to OpenAI servers
* Note it needs minimal of 1 GB of RAM
[Link](https://www.toolify.ai/gpts/unveiling-the-accuracy-of-openai-whisper-on-raspberry-pi-331506)
[Python install](https://pypi.org/project/openai-whisper/)
* Working directly by sending audio file to chat is not working !
[Link](https://platform.openai.com/docs/guides/speech-to-text/improving-reliability)

### TODO
* Minimize lags , Use OpenAI [Realtime API](https://platform.openai.com/docs/guides/realtime)
* Use fast STT module from [Replicate](https://replicate.com/)
* UI - Add LED to indicate actions.

## Feedback
If you have any feedback, please reach out to us at shmulik.debby@gmail.com