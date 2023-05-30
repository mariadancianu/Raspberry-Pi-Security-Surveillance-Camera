# Raspberry-Pi-Security-Alarm-System
A simple security alarm system to detect intruders using a Raspberry Pi 4. 

Steps:
- motion detection with PIR sensor;
- camera activation when a movement is detected;
- camera captures an image and saves it as a jpg in a pre-defined folder; the name of the image contains the timestamp when the image was captured;
- apply face detection on the captured image; 
- if a face is detected, apply face recognition;
- if the face is not recognized, send an alert email to the user, including the captured image.


## Tools and technologies

### Hardware 
- Raspberry Pi 4
- Raspberry Pi compatible camera module 
- Micro SD Card
- Passive Infrared (PIR) motion sensor 
- Mouse, keyboard, HDMI cable, computer monitor  

### Software 
Python version: 3.9. 

Python main libraries:
- opencv
- picamera2
- gpiozero
- smtpblib
- email


## Status
Project is: *in progress*. 

## Helper documentation and references
- Install the Raspbian OS in your Raspberry Pi ([Getting started with Raspberry Pi](https://www.raspberrypi.com/documentation/computers/getting-started.html))
- Plug the camera into the Raspberry Pi and enable the camera port ([Install a Camera on your Raspberry Pi: The Ultimate Guide](https://raspberrytips.com/install-camera-raspberry-pi/))
- Connect the PIR motion sensor to the correct Raspberry Pi GPIO (General Purpose Input-Output) pins ([Connect the PIR motion sensor](https://projects.raspberrypi.org/en/projects/parent-detector/1))

## Contact 
Created by mary_0094@hotmail.it, feel free to get in touch! :woman_technologist:
