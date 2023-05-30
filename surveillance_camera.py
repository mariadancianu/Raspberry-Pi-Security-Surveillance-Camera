import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
import datetime
import cv2 as cv

from picamera2 import Picamera2, Preview 
from gpiozero import MotionSensor


sender_address = ""
sender_password = ""

receiver_address = "mary_0094@hotmail.it"
path_to_images = ""


def prepare_email_content(image_timestamp):
    """Prepares the content of the email to be sent.
    Adds also the photo captured by the camera. 

    Args:
      image_timestamp:
    
    Returns:
      email_content:
      
    """
    
    email_content = EmailMessage()
    
    email_subject = "Warning from surveillance camera"
    
    email_content['Subject'] = email_subject
    email_content['From'] = sender_address
    email_content['To'] = receiver_address

    email_content.set_content("Warning from surveillance camera!")
    
    # attach the photo to the email
    attachment_filename = f"{path_to_images}/surveillance_camera_{image_timestamp}.jpg"
    attachment_cid = make_msgid(domain='xyz.com')
   
    email_content.add_alternative("""\
    <html>
        <body>
            <p>Someone entered your house!<br>
            </p>
            <img src="cid:{attachment_cid}">
        </body>
    </html>
    """.format(attachment_cid=attachment_cid[1:-1]), subtype='html')

    with open(attachment_filename, 'rb') as img:
        maintype, subtype = mimetypes.guess_type(
            img.name)[0].split('/')

        email_content.get_payload()[1].add_related(
            img.read(),
            maintype=maintype,
            subtype=subtype,
            cid=attachment_cid
        )
        
    return email_content


def send_email(image_timestamp):
    """Sends an email to a pre-defined email address
    including a photo attachment.
    
    Args:
      image_timestamp:
    
    """
  
    email_smtp = "smtp.gmail.com"
   
    email_content = prepare_email_content(image_timestamp)
   
    server = smtplib.SMTP(email_smtp, '587')
    
    server.ehlo()
    server.starttls()
    
    server.login(sender_address, sender_password)
    server.send_message(email_content)
    
    server.quit()
    
    print(f"Alert email was sent to {receiver_address}")
    
    return


def capture_image():
    """Captures an image and saves it as a jpg file with the name 
    of the timestamp when the image was captured.  
    """
    
    camera = Picamera2()

    config = camera.create_preview_configuration(main={"size": (1600, 1200)})

    camera.configure(config)

    camera.start()
    
    photo_timestamp = datetime.datetime.now()
    
    camera.capture_file(f"{path_to_images}/surveillance_camera_{image_timestamp}.jpg")

    camera.close()

    return photo_timestamp 


def detect_face(image_timestamp):
     """Detects faces in an image applying the Open CV pretrained model
     Haar Cascade Classifier. 
     
     Args:
       image_timestamp:
    
     Returns:
       face_detected: boolean
         True if a face was detected in the image, False otherwise.
     """
     
     imagePath = f"{path_to_images}/surveillance_camera_{image_timestamp}.jpg"
     img = cv.imread(imagePath)
     
     # convert to grayscale (computationally more efficient)
     gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
     
     face_classifier = cv.CascadeClassifier(
        cv.data.haarcascades + "haarcascade_frontalface_default.xml")
     
     # face detection with pre-trained model
     face = face_classifier.detectMultiScale( # identifies faces of different sizes
        gray_image, #the image 
        scaleFactor=1.1, #?
        minNeighbors=5, #?
        minSize=(40, 40) #?
     )
     
     if len(face) == 0:
        face_detected = False
     else:
        face_detected = True
        
        print("Face detected!")
        
     return face_detected


def recognize_face():
    """
    
    Returns:
      face_recognized: boolean
        True if a face detected in the image is recognized, False otherwise.
    """
    
    face_recognized = True
    
    return face_recognized


def facial_recognition():
    """
    
    Returns:
      intruder_alert: boolean
         True if an intruder was detected and an alert should be sent 
         to the user, False otherwise. 
    """
     
    intruder_alert = False
    
    face_detected = detect_face()
    
    if face_detected:
        face_recognized = recognize_face()
        
        if not face_recognized:
            intruder_altert = True
            
    return intruder_alert


def SurveillanceCamera():
    """Surveillance camera, activated by a motion sensor. When a movement is 
    detcted, the camera is activated and an image is captured and saved. The 
    image is then subject to face detection and face recognition. If the face 
    is not recognized, an alert is sent to the user email, including the image
    of the intruder. """
    
    # TODO: activate camera only in case of motion detected by PIR sensor
    # TODO: apply face recognition
    
    # pir = MotionSensor(3)

    print("Capturing the photo")
    
    photo_timestamp = capture_image()
    
    print("Done!")
    
    print("Facial recognition")
    
    intruder_alert = facial_recognition()
    
    print("Done!")
    
    if intruder_alert:
        print("Sending the alert email")
    
        _ = send_email(photo_timestamp)
    
        print("Done!")
    
    return


if __name__ == '__main__':
    SurveillanceCamera()
