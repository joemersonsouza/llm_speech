import requests
from gtts import gTTS
import speech_recognition as sr
import vlc
import os
import time

url = "http://localhost:8000/v1/chat/completions"
language = "en"
DONE = 6
player = vlc.MediaPlayer()

# This method is used to do a request to the LLM API
# You can change the MAX_TOKENS to change the length of the response
# The parameter MODEL is the name of the model you want to use, you can find the available models in the ILACOL documentation
def get_response(message):
    body = { "messages": [{"role": "user", "content": message}], "model": "llama-2-7b-chat.ggmlv3.q4_0.bin", "stream": False, "temperature": 0.7, "max_tokens": 500}
    result = requests.post(url, json=body).json()
    return result["choices"][0]["message"]["content"]

# This method is used to play the audio file
def play_audio(filename):
    media = vlc.Media(filename)
    player.set_media(media)
    player.play()
    current_state = player.get_state()
    while current_state != DONE:
        current_state = player.get_state()
        time.sleep(0.5)
        
# This method is used to generate the audio file
def generate_audio(text, filename="temp.mp3"):
    tts = gTTS(text, lang=language)
    tts.save(filename)
    return filename

# This method is used to listen to the LLM response based on the user's input
# It calls the get_response method to get the response from the LLM API
# And then generates the audio file based on the response
# Finally, it plays the audio file
def listen(question):
    response = get_response(question)
    audio = generate_audio(response)
    play_audio(audio)

# This method is used to listen to the user's input
def talk():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        speach = recognizer.listen(mic)
        speachToText = recognizer.recognize_google(speach).lower()
        print(speachToText)
        return speachToText

# You can stop the program by saying "stop"
if __name__ == "__main__":
    errorMessage = generate_audio("Sorry I didn't get that", "errorMessage")
    okMessage = generate_audio("Ok, wait a minute", "okMessage")

    while True:
        try:
            text = talk()
            if not text:
                play_audio(errorMessage)
                time.sleep(1)
            elif text == "stop":
                if(player.is_playing()): # TODO: Make the listening asychronous and stop the player when the user says "stop"
                    player.stop()
                else:
                    break
            else:
                play_audio(okMessage)
                listen(text)
        except Exception as e:
            play_audio(errorMessage)
            print(e)
            time.sleep(1)

    os.remove(errorMessage)
    os.remove(okMessage)
    