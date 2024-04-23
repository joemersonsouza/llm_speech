from gtts import gTTS
import speech_recognition as sr
import vlc
import os
import time

player = vlc.MediaPlayer()
language = "en"
DONE = 6

def play_audio(filename, removeAtEnd=True):
    media = vlc.Media(filename)
    player.set_media(media)
    player.play()
    current_state = player.get_state()
    while current_state != DONE:
        current_state = player.get_state()
        time.sleep(0.5)
    if(removeAtEnd):
        os.remove(filename)

# This method is used to generate the audio file
def generate_audio(text, filename="temp.mp3"):
    tts = gTTS(text, lang=language)
    tts.save(filename)
    return filename