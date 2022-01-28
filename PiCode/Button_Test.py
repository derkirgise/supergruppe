import RPi.GPIO as GPIO
import time
def button():
    GPIO.setmode(GPIO.BCM)
    buttonPin = 23
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    buttonPfuschCount=0;
    while True:
        buttonState = GPIO.input(buttonPin)
        #button Pfusch
        if buttonState==GPIO.HIGH:
            print("high")
        else:
            print("low")

        time.sleep(0.2)
button()