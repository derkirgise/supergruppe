import json

class WeatherData:

    def __init__(self, temperature, pressure, altitude, datetime):
        self.temperature = temperature
        self.pressure = pressure
        self.altitude = altitude
        self.datetime = datetime

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
            