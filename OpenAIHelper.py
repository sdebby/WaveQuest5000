import os
from openai import BadRequestError, OpenAI

import requests
MyApi_key=os.environ['OpenAI_Key']
client = OpenAI(api_key=MyApi_key)

class OpenAIHelper:

    def TextToImg(input:str, format:str, Imgstyle:str = 'vivid', ImgSize:str = '1024x1024'):
        """
        Open AI text to image\n
        Using dall-e-3 model, image size 1024X1024\n
        - input : text input\n
        - format : response format url or b64_json\n
        - ImgSize : response image size  1024x1024, 1792x1024 or 1024x1792\n
        - ImgStype : natural or vivid\n
        Return image URL /  base64 json
        """
        response = client.images.generate(
        model="dall-e-3",
        prompt=input,
        response_format=format,
        size= ImgSize,
        style=Imgstyle,
        quality="standard", #standard or hd
        n=1, # number of images netween 1 to 1
        )

        image_response = response.data[0]
        if format == "url":
            return image_response.url
        elif format == "b64_json":
            return image_response.b64_json
        else :
            print('Format dont mach')
    
    def SaveImageFromB64(B64Input:str, OutputName:str):
        """
        Save image from Base64 stream\n
        - B64Input : Base64 input stream image\n
        - OutputName : Output file name
        """
        import base64
        imgdata = base64.b64decode(B64Input)
        with open(OutputName, 'wb') as f:
            f.write(imgdata)
        print('Image saved from base64: '+OutputName)

    def SaveImageFromURL(urlInput:str, OutputName:str):
        """
        Save image from URL\n
        - urlInput : URL image\n
        - OutputName : Output file name
        """
        response = requests.get(urlInput)
        if response.status_code == 200:
            with open(OutputName, "wb") as file:
                file.write(response.content)
            print('Image saved from URL: '+OutputName)
        else:
            print("Failed to download the image. Status code:", response.status_code)    

    def TTS(input:str,outputFile:str,voice:str):
        """
        Open AI Text To Speach - Save audio to file\n
        - input : text input\n
        - outputFile : file path and name for output\n
        - voice - Chose form : 'alloy','echo','fable','onyx','nova','shimmer'
        """
        AIModel=['tts-1','tts-1-hd']
        response = client.audio.speech.create(
            model=AIModel[0],
            voice=voice,
            response_format='wav',
            speed=0.94,
            input=input,)
        response.stream_to_file(outputFile)
        print('Sending Text to speach')

    def TTSStream(inputText:str,voice:str):
        """
        Open AI Text To Speach using stream to output voice\n
        - inputText : text input\n
        - voice - Chose form : 'alloy','echo','fable','onyx','nova','shimmer'
        """
        import pyaudio
        p = pyaudio.PyAudio()
        stream = p.open(format = 8,
                        channels = 1,
                        rate = 24_000,
                        frames_per_buffer = 2048,
                        output_device_index = 2,
                        output=True)
        AIModel=['tts-1','tts-1-hd']
        with client.audio.speech.with_streaming_response.create(
                model=AIModel[0],
                voice=voice,
                input=inputText,
                speed=0.94,
                response_format="pcm") as response:
            for chunk in response.iter_bytes(2048):
                stream.write(chunk)

    def TTSStreamConvert(inputText:str, voice:str, buffer:int, NewSampleRate:int = 48000):
        """
         Open AI Text To Speach using stream to output voice\n
         Converting sample rate to new sample rate (can be used on Raspberry pi) when needed different sample rate output\n
        - inputText : text input\n
        - voice :  Chose form : 'alloy','echo','fable','onyx','nova','shimmer'\n
        - buffer : The buffer in bytes
        - NewSampleRate : The new sample rate to convert
        """
        from pydub import AudioSegment
        import pyaudio
        p = pyaudio.PyAudio()
        stream = p.open(format = pyaudio.paInt16,
                        channels = 1,
                        rate = 48000,
                        frames_per_buffer = 2048,
                        output_device_index = 0,
                        output=True)

        with client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice=voice,
                input=inputText,
                speed=0.94,
                response_format="pcm"
        ) as response:
            pcm_data = bytearray()
            for chunk in response.iter_bytes(buffer):
                pcm_data.extend(chunk)
                audio_segment = AudioSegment(
                data=pcm_data,
                sample_width = 2,  # 2 bytes for int16
                frame_rate = 24000,  # original sample rate is 24000 Hz (PCM)
                channels = 1)
                resampled_audio = audio_segment.set_frame_rate(NewSampleRate)
                raw_audio_data = resampled_audio.raw_data
                stream.write(raw_audio_data)

        stream.stop_stream()
        stream.close()

    def Chat(ChatModel:str,temp:float,max_tok:int,msglist:list):
        """
        Open AI Chat GPT response\n
        - ChatModel : Open AI chat model (like gpt-4)\n
        - temp : chat temprature (creativity)- can set to 0.7\n
        - max_tok :  the maximum tokens alowed.\n
        - msglist : The message in json format.
        """
        response = client.chat.completions.create(
            model=ChatModel,
            temperature=float(temp),
            max_tokens=max_tok,
            messages=msglist)
        Result=response.choices[0].message.content
        print('Sending Text to Chat model: '+ChatModel)
        return Result
    
    def STT(file:str):
        """
        Open AI Speach to text\n
        - file : the audio file to transcript.\n
        Return .text='err' if get error
        """
        audio_file= open(file, "rb")
        print('Sending Speach to text')
        try:
            transcript = client.audio.translations.create( model="whisper-1", file=audio_file)
        except BadRequestError as err: # Get error
            print(err.body["message"])
            class ERR:
                text = "err"
            transcript = ERR()
        return transcript
    
    def EncodeImage(FN:str):
        """
        Encode image to base64\n
        - FN : input image file name\n
        """
        import base64
        with open(FN, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def ImageResponse(InageBase64:str,ChatModel:str,max_tok:int,UsrText:str):
        """
        OpenAI image analyse\n
        - InageBase64 : Input image converted to base64\n
        - ChatModel : The OpenAI model\n
        - max_tok : Maxinum tokens to use\n
        - UsrText : User text to ask about the image
        """
        headers = {
        "Content-Type": "application/json", "Authorization": f"Bearer {MyApi_key}"
        }

        payload = {
        "model": ChatModel,
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": UsrText
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{InageBase64}",
                    "detail": "auto"
                }
                }
            ]
            }
        ],
        "max_tokens": max_tok
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        MyRes = response.json()
        ResKeys = Get3=list(MyRes.keys())
        if ResKeys[0] == 'error':
            print('ImageResponse - ERROR')
            return MyRes.get('error').get('message')
        else:
            return MyRes.get('choices')[0].get('message').get('content')