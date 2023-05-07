import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes

from picamera2 import Picamera2, Preview 
from gpiozero import MotionSensor


sender_address = ""
sender_password = ""

receiver_address = "mary_0094@hotmail.it"


def prepare_email_content():
    """Prepares the content of the email to be sent.
    Adds also the photo captured by the camera. 

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
    attachment_filename = "/home/pi/Desktop/image.png"
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


def send_email():
    """Sends an email to a pre-defined email address
    including a photo attachment."""
  
    email_smtp = "smtp.gmail.com"
   
    email_content = prepare_email_content()
   
    server = smtplib.SMTP(email_smtp, '587')
    
    server.ehlo()
    server.starttls()
    
    server.login(sender_address, sender_password)
    server.send_message(email_content)
    
    server.quit()
    
    print(f"Alert email was sent to {receiver_address}")
    
    return


def capture_photo():
    """ 
    """
    
    camera = Picamera2()

    config = camera.create_preview_configuration(main={"size": (1600, 1200)})

    camera.configure(config)

    camera.start()

    camera.capture_file("test-python.jpg")

    camera.close()

    return 


def SurveillanceCamera():
    """
    """
    
    # TODO: activate camera only in case of motion detected by PIR sensor
    # TODO: apply face recognition/human vs animal algorithms     
    # pir = MotionSensor(3)

    print("Capturing the photo")
    
    _ = capture_photo()
    
    print("Done!")
    
    print("Sending the alert email")
    
    _ = send_email()
    
    print("Done!")
    
    return


if __name__ == '__main__':
    SurveillanceCamera()
