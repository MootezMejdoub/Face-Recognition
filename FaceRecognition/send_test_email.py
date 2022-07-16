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
    root = tk.Tk()
    root.title("Mootez's App")
    canvas = tk.Canvas(root, width=500, height=200, bg='sky blye')
    canvas.grid(columnspan=3, rowspan=3)
    root.configure(bg='sky blue')
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
            if(Id==2 and conf<50):
                Id="OBAMA"
            elif(Id==1 and conf<70):
                Id=name
                #Id="mootez"
            else:
                Id="Unknown"

            # Put text describe who is in the picture
            
            cv2.putText(im, str(Id), (x,y-40), font, 2, (255,255,255), 3)
            

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
