#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

RED=0xFF0000
GREEN=0x00FF00
BLUE=0x0000FF



pins = {'pin_R':17, 'pin_G':18, 'pin_B':27}
#pins = {'pin_R':11, 'pin_G':12, 'pin_B':13} # pins is a dict

GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
for i in pins:
	GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
	GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
p_G = GPIO.PWM(pins['pin_G'], 2000)
p_B = GPIO.PWM(pins['pin_B'], 2000)

p_R.start(0)      # Initial duty Cycle = 0(leds off)
p_G.start(0)
p_B.start(0)

doBlink = True;

def calcPercentage(value):
    return int(100-(value/255)*100)

def setColor(col):   # For example : col = 0x112233
	R_val = (col & 0xff0000) >> 16
	G_val = (col & 0x00ff00) >> 8
	B_val = (col & 0x0000ff) >> 0
	#print(R_val,G_val,B_val)
	R_val = calcPercentage(R_val)
	G_val = calcPercentage(G_val)
	B_val = calcPercentage(B_val)
	
	
	p_R.ChangeDutyCycle(R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(G_val)
	p_B.ChangeDutyCycle(B_val)

def stopBlink():
    doBlink = False
    #print("Method called: " + str(doBlink))

def blink():
    while doBlink:
        #print(doBlink)
        setColor(RED)
        time.sleep(0.5)
        setColor(BLUE)
        time.sleep(0.5)
'''
try:
	while True:
		for col in colors:
			setColor(col)
			time.sleep(2)
except KeyboardInterrupt:
	p_R.stop()
	p_G.stop()
	p_B.stop()
	for i in pins:
		GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
	GPIO.cleanup()'''