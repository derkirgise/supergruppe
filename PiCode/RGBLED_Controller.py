#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

pins = {'pin_R':17, 'pin_G':18, 'pin_B':27}

GPIO.setmode(GPIO.BCM)
for i in pins:
	GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
	GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
p_G = GPIO.PWM(pins['pin_G'], 2000)
p_B = GPIO.PWM(pins['pin_B'], 2000)

p_R.start(0)      # Initial duty Cycle = 0(leds off)
p_G.start(0)
p_B.start(0)

def calcPercentage(value):
    return int(100-(value/255)*100)

def setColor(col):   # For example : col = 0x112233
	R_val = (col & 0xff0000) >> 16
	G_val = (col & 0x00ff00) >> 8
	B_val = (col & 0x0000ff) >> 0
	
	R_val = calcPercentage(R_val)
	G_val = calcPercentage(G_val)
	B_val = calcPercentage(B_val)
	
	p_R.ChangeDutyCycle(R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(G_val)
	p_B.ChangeDutyCycle(B_val)
