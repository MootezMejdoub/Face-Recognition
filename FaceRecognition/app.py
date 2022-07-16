from tkinter import *
import tkinter as tk
import tkinter.font
from PIL import Image
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import sys
import os
import tkinter.messagebox
import cv2
import time
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import numpy as np
import requests
import time
root = tk.Tk()
root.title("Mootez's App")
canvas = tk.Canvas(root, width=800, height=0)
canvas.grid(columnspan=3, rowspan=3)
root.configure(bg='#530332')




#logo
logo = Image.open('image1.jpg')
#resize taswiriti
resized =logo.resize((400, 500), Image.ANTIALIAS)
newlogo = ImageTk.PhotoImage(resized)
logo_label = tk.Label(image=newlogo)
logo_label.image =resized
logo_label.grid(column=1,rowspan=3, row=0)


#instruction
instructions = tk.Label(root, text="Bienvenue dans notre application", bg="pink",fg="black", height=2, width=40, font="Raleway")
instructions.grid(columnspan=1, rowspan=3, column=1, row=3)



def run():
    vid_cam = cv2.VideoCapture(0)

# Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    name = askstring('Name', 'What is your name?')
# For each person, one face id
#face_id =1
    face_id= input("donner le numero ID")
# Initialize sample face image
    count = 0

# Start looping
    while(True):

    # Capture video frame
        _, image_frame = vid_cam.read()

    # Convert frame to grayscale
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    # Detect frames of different sizes, list of faces rectangles
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # Loops for each faces
        for (x,y,w,h) in faces:

        # Crop the image frame into rectangle
            cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
        
        # Increment sample face image
            count += 1

        # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
    
        # Display the video frame, with bounded rectangle on the person's face
            cv2.imshow('frame', image_frame)

    # To stop taking video, press 'q' for at least 100ms
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    # If image taken reach 100, stop taking video
        elif count>100:
            break

# Stop video
    vid_cam.release()

# Close all started windows
    cv2.destroyAllWindows()

    
    #os.system('python3 face_datasets.py')
    #print('visage bien détecté et prétraité')
def train():
    os.system('python3 training.py')
    print('training completed')
    messagebox.showinfo('Result','Training completed !')
def recognition():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load the trained mode
    recognizer.read('trainer/trainer.yml')
    # Load prebuilt model for Frontal Face
    cascadePath = "haarcascade_frontalface_default.xml"

    def send_message(Id):
        return requests.post("https://api.mailgun.net/v3/sandboxc01ab45d01ae4f5ea6cc18d499141c7e.mailgun.org/messages",
            auth=("api", "6f92e73872c8ff19a28f873df17eae73-2a9a428a-58c4043f"),
            files = [("attachment", ("image.jpg", open("image.jpg", "rb").read()))],
            data={"from": 'hello@example.com',
                "to": ["mootezmejdoub@gmail.com"],
                "subject": "You have a visitor",
                "html": "<html>" + Id + " est présent.  </html>"})
                          
    currentname = "unknown"


    # Create classifier from prebuilt model
    faceCascade = cv2.CascadeClassifier(cascadePath);

    # Set the font style
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize and start the video frame capture
    cam = cv2.VideoCapture(0)

    # Loop
    while True:
        # Read the video frame
        ret, im =cam.read()

        # Convert the captured frame into grayscale
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

        # Get all face from the video frame
        faces = faceCascade.detectMultiScale(gray, 1.2,5)

        # For each face in faces
        for(x,y,w,h) in faces:

            # Create rectangle around the face
            cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if conf<50:
                cv2.putText(im, s , (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                    
            else:
                cv2.putText(im, "UNKNOWN", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)

            

        # Display the video frame with the bounded rectangle
        cv2.imshow('im',im)
        

        # If 'q' is pressed, close program
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Stop the camera
    cam.release()

    # Close all windows
    cv2.destroyAllWindows()

    
    #os.system('python3 face_recognition.py')


btn = Button(root, text="Face Detection", bg="pink", fg="black", height=2, width=13,command=run)
btn.grid(column=0, rowspan=1, row=0)

#boutton mta3 trainning

btn = Button(root, text="training", bg="pink", fg="black", height=2, width=13, command=train)
btn.grid(column=0, rowspan=2, row=0)

#boutton mta3 recognition

btn = Button(root, text="Face Recognition", bg="pink", fg="black", height=2, width=13, command=recognition)
btn.grid(column=0, rowspan=3, row=0)


root.mainloop()
