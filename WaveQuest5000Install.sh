#!/bin/bash

RED = '\033[0;31m'
GREEN = '\033[0;32m'
CYAN = '\033[0;36m'
YELLOW = '\033[1;33m'
NC = '\033[0m' # No Color

echo -e '${YELLOW}WaveQuest5000 PROJECT \n This script will install all nessesery apps efter a fresh RPI install${NC}'

echo ' '
echo -e '${GREEN}Updating machine${NC}'
echo '----------------------------'
sudo apt update
sudo apt upgrade -y

echo ' '
echo -e '${GREEN}Installing virtual enviorment (venv)${NC}'
echo '----------------------------'
python -m venv venv --system-site-packages
source venv/bin/activate 

echo ' '
echo -e '${GREEN}Installing and updating pip${NC}'
echo '----------------------------'
sudo apt install -y python3-pip
pip install --upgrade pip

echo ' '
echo -e '${GREEN}Installing project requirments${NC}'
echo '----------------------------'
pip install playsound==1.2.2 pydub gpiozero sounddevice soundfile openai requests
sudo apt install -y python3-numpy git libportaudio2 ffmpeg python3-pyaudio
sudo apt install -y python3-picamera2 --no-install-recommends

echo ' '
echo -e '${GREEN}Removing unesessery packages${NC}'
echo '----------------------------'
sudo apt autoremove -y

echo ' '
echo ' '
echo -e "${RED}Do not forget to add OpenAI key - nano ~/.profile ;export OpenAI_Key=<OpenAI key>${NC}"
echo 'BYE'