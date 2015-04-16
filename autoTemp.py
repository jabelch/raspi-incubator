import MySQLdb
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Helper function to change pin state
def setPin(pinNumber, dir):
    GPIO.setup(pinNumber, dir, pull_up_down=GPIO.PUD_UP)

#High and Low set points (fahrenheit)
SP_HIGH = 90
SP_LOW = 80
LIGHT = 23
FAN = 24

Heating = 1
Cooling = 2

tempQuery = """
    SELECT `temperature`, `humidity`
    FROM tempdat
    ORDER BY `tdate` DESC, `ttime` DESC
    LIMIT 1
"""
setpointQuery = """
    SELECT `sp_high`, `sp_low`
    FROM setpoints
    WHERE `id` = 1
"""

def getData():
    #Grab the latest reading from database
    db = MySQLdb.connect("localhost", "monitor", "raspberry", "temps")
    curs=db.cursor()

    with db:
        curs.execute (tempQuery)

    for (temperature, humidity) in curs:
        results = (temperature, humidity)

    with db:
        curs.execute (setpointQuery)
    sp = []
    for (sp_high, sp_low) in curs:
        sp = (sp_high, sp_low)

    curs.close()
    db.close()

    return results, sp

def autoTemp():
    currentState = Heating
    while(1):
        temp, sp = getData()
        tempC = float(temp[0])
        tempF = 9.0/5.0 * tempC + 32.0
        humid = float(temp[1])
        sp_high = float(sp[0])
        sp_low = float(sp[1])


        #print "TempC : " + str(tempC) + " TempF : " + str(tempF) + " Humid : " + str(humid)
        if (tempF > sp_high):
            #Turn Off Heater
            setPin(LIGHT, GPIO.IN)
            currentState = Cooling
        elif (tempF < sp_low):
            #Turn On Heater
            setPin(LIGHT, GPIO.OUT)
            currentState = Heating

        time.sleep(5)

if __name__ == "__main__":
    autoTemp()
