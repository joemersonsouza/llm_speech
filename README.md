# Speech Recognition and Response Project

This project is a speech recognition system that converts speech into text using Python as the main language. It then uses a Language Model (LM) to generate responses based on user requests. The project also includes the use of VLC for playing MP3 audio files and gTTS for converting the LM responses into audio. The face recognition was made based on https://towardsdatascience.com/real-time-face-recognition-an-end-to-end-project-b738bb0f7348 thanks Marcelo Rovai.

## Dependencies:

This project is using an amazing LLM provided by [IALACOL](https://github.com/chenhunghan/ialacol?tab=readme-ov-file) and [K3S](https://k3s.io/) for containerization.
To have you LLM running, do not forget to forward your kube svc port `kubectl port-forward svc/llama-2-7b-chat 8000:8000`

- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [pydub](https://pypi.org/project/pydub/)
- [gtts](https://pypi.org/project/gTTS/)
- [VLC](https://www.videolan.org/vlc/index.html)

## Usage:

1. Install the dependencies using `pip install -r requirements.txt`
2. Run the `src/llm.py` file to start the speech recognition system
3. Speak into the microphone to make a request
4. The LM will generate a response based on your request
5. The response will be converted into speech using gTTS and played through VLC

## Running in Kubernetes:

This project can be containerized using Kubernetes for easy deployment and management. The LM can be run as a container within a Kubernetes cluster to scale the speech recognition system as needed.

For more information on Kubernetes, visit the [Kubernetes website](https://kubernetes.io/)

## Do you want support?

Create some MR to improve this code :-) 

## Disclaimer:

This project is for demonstration purposes only and may not be suitable for production use. It is recommended to thoroughly test and customize the code for your specific use case.
