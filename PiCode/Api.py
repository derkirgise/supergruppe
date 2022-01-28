from WeatherData import WeatherData
import flask
import sys
from flask_cors import CORS, cross_origin
from DatabaseConnection import getWeatherData
from Sensor_Controller import getWeather, getTemp
print(sys.path)
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = False


@app.route('/weatherdata', methods=['GET'])
def weatherdata():
    return getWeatherData()

@app.route('/weatherstring', methods=['GET'])
def weatherstring():
    return getTemp() + " & " + getWeather()

app.run(host='0.0.0.0', port=5001)



