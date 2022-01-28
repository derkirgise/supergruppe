import RPi.GPIO as GPIO
import adafruit_bmp280
import time
import threading
import mariadb
from DatabaseConnection import logWeatherData
from Sensor_Controller import getTemp, getWeather,readSensor
from LED_Controller import show_message
from RGBLED_Controller import setColor
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, ATARI_FONT

#Initialise temperature/pressure-sensor
adafruit_bmp280.sea_level_pressure = 1035.09
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)

#Initialise LED-matrix
device.contrast(1)
view = viewport(device, width=32, height=8)

#Define LED-lamp function
def blink():
    while True:
        if getWeather()=="regnerisch":
            setColor(0x00FFFF)
            time.sleep(0.5)
            setColor(0x0000FF)
            time.sleep(0.5)
        elif getWeather()=="sonnig":
            setColor(0xFFFF00)
        elif getWeather()=="bewölkt":
            setColor(0xFFFFFF)

#Start LED-lamp-thread
blinkThread = threading.Thread(target=blink)
blinkThread.start()

#Define button function
def button():
    buttonPin = 23
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        data = readSensor()
        temperature = str(data[0]) + " C"
        pressure = str(data[1]) + " hPa"
        altitude = str(data[2]) + " m"
        buttonState = GPIO.input(buttonPin)

        if buttonState == False:
            show_message(device, getTemp() + " & " + getWeather(), fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)
        else:
            show_message(device, temperature, fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)
            show_message(device, pressure, fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)
            show_message(device, altitude, fill="white", font=proportional(LCD_FONT), scroll_delay=0.08)
        time.sleep(0.2)

#Start button-thread
buttonThread = threading.Thread(target=button)
buttonThread.start()

#Define database-function
def logData():
    while True:
        data=readSensor()
        logWeatherData(data)

#Start database-thread
DBThread = threading.Thread(target=logData)
DBThread.start()
