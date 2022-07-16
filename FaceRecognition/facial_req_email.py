# Import OpenCV2 for image processing
import cv2

# Import numpy for matrices calculations
import numpy as np
import requests
import time

# Create Local Binary Patterns Histograms for face recognization
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
        if(Id==1 and conf<50):
            Id="Mootez"
            if currentname != Id:
                currentname = Id
                time.sleep(1.0)
                img_name = "image.jpg"
                cv2.imwrite(img_name, im)
                print('Taking a picture.')
                
                request = send_message(Id)
                print ('Status Code: '+format(request.status_code)) #200 status code means email sent successfully
        elif(Id==2 and conf<70):
            Id="obama"
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
