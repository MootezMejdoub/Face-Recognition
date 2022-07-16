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
import mysql.connector
#tarki7 lwindow mta33 l app
root = tk.Tk()
root.title("Mootez's App")
canvas = tk.Canvas(root, width=800, height=0)
canvas.grid(columnspan=3, rowspan=5)
root.configure(bg='#530332')
#logo
logo = Image.open('image1.jpg')
#resize taswiriti
resized =logo.resize((400, 500), Image.ANTIALIAS)
newlogo = ImageTk.PhotoImage(resized)
logo_label = tk.Label(image=newlogo)
logo_label.image =resized
logo_label.grid(column=1,rowspan=3, row=0)




#training
def train():
    os.system('python3 training.py')
    print('training completed')
    messagebox.showinfo('Done','Training completed !')




#dataset
def detection():
     if (t1.get()==""):
         messagebox.showinfo("Error","Please insert the user Name...")
         #showerror("Error", "Please insert the use Name!")
         
     else:
        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "raspberry",
            database = "STUDENTS"
            )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * from stu_table")
        myresult = mycursor.fetchall()
        id = 1
        for x in myresult:
            id +=1
        
        sql = "insert into stu_table(id,name) values(%s, %s)"
        val = (id, t1.get())
        mycursor.execute(sql,val)
        mydb.commit()
        vid_cam = cv2.VideoCapture(0)
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        count = 0
        while(True):

            # Capture video frame
            _,image_frame = vid_cam.read()

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
                cv2.imwrite("dataset/User." + str(id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

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
        messagebox.showinfo('Result','Face detection completed !')

        
#reconnaissance

def recognition():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load the trained mode
    recognizer.read('trainer/trainer.yml')
    # Load prebuilt model for Frontal Face
    cascadePath = "haarcascade_frontalface_default.xml"
    #mta3 l mail
    def send_message(s):
        return requests.post("https://api.mailgun.net/v3/sandboxc01ab45d01ae4f5ea6cc18d499141c7e.mailgun.org/messages",
            auth=("api", "6f92e73872c8ff19a28f873df17eae73-2a9a428a-58c4043f"),
            files = [("attachment", ("image.jpg", open("image.jpg", "rb").read()))],
            data={"from": 'hello@example.com',
                "to": ["mootezmejdoub@gmail.com"],
                "subject": "You have a visitor",
                "html": "<html>" + s + " est présent.  </html>"})
        
                          
    currentname = "unknown"


    # Create classifier from prebuilt model
    faceCascade = cv2.CascadeClassifier(cascadePath);

    # Set the font style
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize and start the video frame capture
    cam = cv2.VideoCapture(0)

    # Loop
    while True:
        # fenetre mta3 l video
        ret, im =cam.read()

        # Convert l l gris
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

        # Get all face from the video frame
        faces = faceCascade.detectMultiScale(gray, 1.2,5)

        # For each face in faces
        for(x,y,w,h) in faces:

            # ta3mel rectangle around the face
            cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
            id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            
            
            mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "raspberry",
            database = "STUDENTS"
            )
            mycursor = mydb.cursor()
            
            mycursor.execute("select name from stu_table where id=" + str(id))
            s = mycursor.fetchone() #tuple
            
            s  = ''+''.join(s) # bech nrodouhq string 

            

            if conf<50:
                #cv2.putText(im, s , (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cv2.LINE_AA)
                cv2.putText(im, s , (x,y-40), font, 2, (255,255,255), 3)
                if currentname != s:
                    currentname = s
                    time.sleep(1.0)
                    img_name = "image.jpg"
                    cv2.imwrite(img_name, im)
                    print('Taking a picture.')
                
                    request = send_message(s)
                    print ('Status Code: '+format(request.status_code)) #200 ma3naha email sent
                    
            else:
                cv2.putText(im, "UNKNOWN", (x,y-40), font, 2, (0,0,255), 3)
                #cv2.putText(im, "UNKNOWN", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)        # Display the video frame with the bounded rectangle
        cv2.imshow('im',im)
        

        # If 'q' programme yetsakar
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Stop  camera
    cam.release()

    # Close all windows
    cv2.destroyAllWindows()




#          ktiba loutania bienvenue
instructions = tk.Label(root, text="Welcome to my face recognition App", bg="pink",fg="black", height=2, width=40, font="Raleway")
instructions.grid(columnspan=1, rowspan=3, column=1, row=3)
# boutton mta3 detection
btn = Button(root, text="Add user", bg="pink", fg="black", height=2, width=13,command=detection)
btn.grid(column=0, rowspan=1, row=0)
#champs mta3 esmi
l1 = tk.Label(root, text="Name:",font=("Algerian",17), bg="pink", fg="black")
l1.grid(column=0, rowspan=2, row=0, sticky=W)
t1 = tk.Entry(root, width=14, bd=5,bg="pink")
t1.grid(column=0, rowspan=2, row=0,sticky=E)
#boutton mta3 trainning
btn = Button(root, text="Training", bg="pink", fg="black", height=2, width=13, command=train)
btn.grid(column=0, rowspan=4, row=1)
#boutton mta3 recognition
btn = Button(root, text="Face Recognition", bg="pink", fg="black", height=2, width=13, command=recognition)
btn.grid(column=0, rowspan=3, row=2)





root.mainloop()
