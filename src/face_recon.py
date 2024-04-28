#https://towardsdatascience.com/real-time-face-recognition-an-end-to-end-project-b738bb0f7348

import time
import cv2
from face_dataset import process_user_recognition
from speech import generate_audio, play_audio

maximumFaces = 30
faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
dataCascade = 'data/trainer.yml'
facesPath = 'data/face'

def say_hello(user):
    play_audio(generate_audio(f"Hello {user} how are you?"))

def test_cam():
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]  
        cv2.imshow('video',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()

def recongnize_face():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read(dataCascade)
    except:
        play_audio(generate_audio(f"Sorry I could not recognize your face, let's do it together"))
        process_user_recognition()
        time.sleep(1)
        recognizer.read(dataCascade)
    
    userName = ""
    with open("data/user.txt", "r") as f:
        userName = f.read()
    
    id = 0
    names = ['None', userName] 
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    greetings = False

    while True:
        ret, img =cam.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        for(x,y,w,h) in faces:
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            # If confidence is less them 100 ==> "0" : perfect match 
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.imshow('camera',img) 

        if(not greetings and id != 0):
            say_hello(id)
            greetings = True

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    cam.release()
    cv2.destroyAllWindows()