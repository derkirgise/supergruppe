#!/usr/bin/env python

import adafruit_bmp280
import board

i2c = board.I2C()
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

def readSensor():
    temperature = round(bmp280.temperature,1)
    pressure = round(bmp280.pressure,1)
    altitude = round(bmp280.altitude,1)
    result = [temperature,pressure,altitude]
    return result

def getWeather():
    pressure=bmp280.pressure
    if pressure<995:
        return "regnerisch"
    elif pressure<1025:
        return "bewölkt"
    else:
        return "sonnig"
    
def getTemp():
    temperature=bmp280.temperature
    if temperature < 15:
        return "Kalt"
    elif temperature < 25:
        return "Mild"
    else:
        return "Warm"
        