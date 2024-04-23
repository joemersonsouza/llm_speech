import numpy as np
import cv2
from PIL import Image
import os
from speech import generate_audio, play_audio

maximumFaces = 30
faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
dataCascade = 'data/trainer.yml'
facesPath = 'data/face'

def warn_user(message):
    play_audio(generate_audio(message))

def generate_user_images():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height
    face_id = 1
    count = 0

    while(count <= maximumFaces):
        ret, img = cam.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite(f"{facesPath}/User.{face_id}.{count}.jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
            if(count == maximumFaces / 2):
                warn_user("You are doing a great job. I'm close to the end of the process")

    cam.release()
    cv2.destroyAllWindows()

# function to get the images and label data
def get_images_labels():
    imagePaths = [os.path.join(facesPath,f) for f in os.listdir(facesPath)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = faceCascade.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids

def face_dataset_train():
    # Path for face image database
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    faces,ids = get_images_labels()
    recognizer.train(faces, np.array(ids))
    # Save the model into trainer/trainer.yml
    recognizer.write(dataCascade) 
    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

def process_user_recognition():
    warn_user("Initializing face capture. Look the camera, move your head, smile, you are being recorded")
    generate_user_images()
    warn_user("Amazing work, now, let me understand you better")
    face_dataset_train()
    warn_user("I'm done, thank you for your time")