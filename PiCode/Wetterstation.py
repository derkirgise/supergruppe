
import RPi.GPIO as GPIO

import adafruit_bmp280
import time
import threading
import mariadb

from Sensor_Controller import getTemp, getWeather,readSensor
from LED_Controller import show_message
from RGBLED_Controller import setColor
 
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, ATARI_FONT

adafruit_bmp280.sea_level_pressure = 1035.09
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)

device.contrast(1)
view = viewport(device, width=32, height=8)


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

blinkThread = threading.Thread(target=blink)
blinkThread.start()



def button():
    buttonPin = 23
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        with canvas(view) as draw:
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

buttonThread = threading.Thread(target=button)
buttonThread.start()

'''
def connectSQL():
    conn = mariadb.connect(
            user = "pi",
            password="supergruppe",
            host="127.0.0.1",
            port=3306,
            database="WeatherLog")
    cursorDb = conn.cursor()
    return [cursorDb, conn];
'''

def logData():
    conn = mariadb.connect(
            user = "pi",
            password="supergruppe",
            host="127.0.0.1",
            port=3306,
            database="WeatherLog")
    cursorDb = conn.cursor()
    while True:
        data=readSensor()
        temperature = data[0]
        pressure = data[1]
        altitude = data[2]
        sqlscript="INSERT INTO Daten (temperature, pressure, altitude, datetime) values ({0}, {1}, {2}, NOW())".format(temperature, pressure, altitude)
        cursorDb.execute(sqlscript)
        conn.commit()
        time.sleep(60)

DBThread = threading.Thread(target=logData)
DBThread.start()
