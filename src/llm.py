import requests
from gtts import gTTS
import vlc
import os
import time
from face_recon import recongnize_face
import threading

from speech import talk

url = "http://localhost:8000/v1/chat/completions"
language = "en"
DONE = 6
player = vlc.MediaPlayer()
waitingLLM = False

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
    waitingLLM = False
    
# You can stop the program by saying "stop"
if __name__ == "__main__":
    errorMessage = generate_audio("Sorry I didn't get that", "errorMessage")
    okMessage = generate_audio("hummmm", "okMessage")
    faceView = threading.Timer(0, recongnize_face)
    faceView.start()

    while True:
        try:
            text = talk()
            if not text:
                time.sleep(1)
            elif text == "stop":
                if(player.is_playing()):
                    player.stop()
                else:
                    play_audio(generate_audio("Press 'ESC' to exit"))
                    break
            else:
                if(waitingLLM): continue

                waitingLLM = True
                play_audio(okMessage)
                llm = threading.Timer(0, listen, args=(text,))
                llm.start()
        except Exception as e:
            print(e)
            time.sleep(1)

    os.remove(errorMessage)
    os.remove(okMessage)
    