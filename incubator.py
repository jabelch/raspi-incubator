from flask import Flask, render_template, request
import datetime
import RPi.GPIO as GPIO
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

# Helper Function to get the current time
def getTime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

@app.route("/")
def main():
    # Read pin state
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    templateData = {
        'pins' : pins,
        'time' : getTime()
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

    templateData = {
        'message' : message,
        'pins' : pins,
        'time' : getTime()
    }

    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

    # Turn pins off when flask finishes
    for pin in pins:
        setPin(pin, GPIO.IN)
