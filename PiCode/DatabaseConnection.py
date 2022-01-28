import mariadb
import json

dbUser = "pi"
dbPassword = "supergruppe"
dbPort = 3306
dbDatabase = "WeatherLog"
dbHost = "127.0.0.1"



# CONNECT TO DATABASE
def getWeatherData():
    weatherData = []

    try:
        conn = mariadb.connect(
        user= dbUser,
        password= dbPassword,
        host= dbHost,
        port= dbPort,
        database= dbDatabase
        )
        cursorDb = conn.cursor()

        cursorDb.execute("SELECT * FROM Daten ORDER BY datetime DESC LIMIT 10")

        for id, temperature, pressure, altitude, datetime in cursorDb:
            dataset = {
                "temperature": temperature,
                "pressure": pressure,
                "altitude": altitude,
                "datetime": datetime
            }
            weatherData.append(dataset)
            
        cursorDb.close()
        conn.close()
            
        return json.dumps(weatherData, indent=4, sort_keys=True, default=str)

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

def logWeatherData(data):
    try:
        conn = mariadb.connect(
        user= dbUser,
        password= dbPassword,
        host= dbHost,
        port= dbPort,
        database= dbDatabase
        )
        cursorDb = conn.cursor()
        
        sqlscript="INSERT INTO Daten (temperature, pressure, altitude, datetime) values ({0}, {1}, {2}, NOW())".format(data[0], data[1], data[2])
        cursorDb.execute(sqlscript)
        conn.commit()
        
        cursorDb.close()
        conn.close()

    except mariadb.Error as b:
        print(f"Error connecting to MariaDB Platform: {b}")
