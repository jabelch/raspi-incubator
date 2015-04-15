#RESTful Server using Flask
from flask import Flask, render_template, request, json

import RPi.GPIO as GPIO
import Adafruit_DHT
import MySQLdb
import sys
import time
import datetime

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

#Create a dictionary of pins
pins = {
    23 : {'name' : 'Lamp', 'state' : GPIO.IN},
    24 : {'name' : 'Fan', 'state' : GPIO.IN}
}

# Helper function to change pin state
def setPin(pinNumber, dir):
    GPIO.setup(pinNumber, dir, pull_up_down=GPIO.PUD_UP)

#Set pins as output and low
for pin in pins:
    setPin(pin, GPIO.IN)

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

@app.route("/")
def main():
    reading = getFromDatabase(1)

    # Read pin state
    for pin in pins:
        pins[pin]['state'] = not GPIO.input(pin)

    templateData = {
        'tdate' : reading[0][0],
        'ttime' : reading[0][1],
        'zone' : reading[0][2],
        'temperature' : reading[0][3],
        'humidity' : reading[0][4],
        'pins' : pins
    }

    return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert pin from URL to integer
    changePin = int(changePin)
    # Get name of device being changed
    deviceName = pins[changePin]['name']
    # Set pin mode
    if action == "on":
        setPin(changePin, GPIO.OUT)
        message = deviceName + " turned on."
    if action == "off":
        setPin(changePin, GPIO.IN)
        message = deviceName + " turned off."
    if action == "toggle":
        setPin(changePin, not GPIO.input(changePin))
        message = "Toggled " + deviceName + "."

    # Read pin state
    for pin in pins:
        pins[pin]['state'] = not GPIO.input(pin)

    #Grab temp from database
    reading = getFromDatabase(1)

    templateData = {
        'tdate' : reading[0][0],
        'ttime' : reading[0][1],
        'zone' : reading[0][2],
        'temperature' : reading[0][3],
        'humidity' : reading[0][4],
        'message' : message,
        'pins' : pins
    }

    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    #turn off pins
    for pin in pins:
        setPin(pin, GPIO.IN)
