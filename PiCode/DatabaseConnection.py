import mariadb
import json

# CONNECT TO DATABASE
def getWeatherData():
    weatherData = []

    try:
        conn = mariadb.connect(
            user="pi",
            password="supergruppe",
            host="127.0.0.1",
            port=3306,
            database="WeatherLog"
        )
        cursorDb = conn.cursor()

        cursorDb.execute("SELECT * FROM Daten ORDER BY datetime ASC LIMIT 10")

        for id, temperature, pressure, altitude, datetime in cursorDb:
            dataset = {
                "temperature": temperature,
                "pressure": pressure,
                "altitude": altitude,
                "datetime": datetime
            }
            weatherData.append(dataset)

        return json.dumps(weatherData, indent=4, sort_keys=True, default=str)

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

def logWeatherData():
     try:
        conn = mariadb.connect(
            user="pi",
            password="supergruppe",
            host="127.0.0.1",
            port=3306,
            database="WeatherLog"
        )
        cursorDb = conn.cursor()

        sqlscript="INSERT INTO Daten (temperature, pressure, altitude, datetime) values ({0}, {1}, {2}, NOW())".format(temperature, pressure, altitude)
        cursorDb.execute(sqlscript)
        conn.commit()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
