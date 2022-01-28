from WeatherData import WeatherData
import flask
import sys
from flask_cors import CORS, cross_origin
from DatabaseConnection import getWeatherData
print(sys.path)
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = False


@app.route('/weatherdata', methods=['GET'])
def weatherdata():
    return getWeatherData()

app.run(host='0.0.0.0', port=80)



