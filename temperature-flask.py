#RESTful Server using Flask
from flask import Flask, render_template, request, json
import Adafruit_DHT
import MySQLdb
import sys
import time
import datetime

app = Flask(__name__)

#Get the top %s temperatures from tempdat 
selectQuery = """
    SELECT `tdate`, `ttime`, `zone`, `temperature`, `humidity`
    FROM tempdat
    ORDER BY `tdate` DESC, `ttime` DESC
    LIMIT %s
"""
def getFromDatabase(numReadings):
    db = MySQLdb.connect("localhost", "monitor", "raspberry", "temps")
    curs=db.cursor()

    with db:
        #Grab the top `numReadings` from the database (newest readings)
        curs.execute (selectQuery, numReadings)
    results = []
    for (tdate, ttime, zone, temperature, humidity) in curs:
        results.append([tdate, ttime, zone, temperature, humidity])

    curs.close()
    db.close()

    return results

def getReading():
    # Attempt to get sensor reading.
    humidity, temp = Adafruit_DHT.read(Adafruit_DHT.DHT11, pin)
    return (humidity, temp)

@app.route("/", methods = ['GET', 'POST'])
def main():
    if request.method == 'GET':
        reading = getFromDatabase(1)
        templateData = {
            'tdate' : reading[0][0],
            'ttime' : reading[0][1],
            'zone' : reading[0][2],
            'temperature' : reading[0][3],
            'humidity' : reading[0][4]
        }
        return render_template('temps.html', **templateData)
    if request.method == 'POST':
        pass
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    #Close cursor and database
