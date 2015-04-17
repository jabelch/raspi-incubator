import MySQLdb
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Helper function to change pin state
def setPin(pinNumber, dir):
    GPIO.setup(pinNumber, dir, pull_up_down=GPIO.PUD_UP)

tempQuery = """
    SELECT `temperature`, `humidity`
    FROM tempdat
    ORDER BY `tdate` DESC, `ttime` DESC
    LIMIT 1
"""
setpointQuery = """
    SELECT `sp_high`, `sp_low`, `sp_too_hot`, `sp_high_h`, `sp_low_h`, `sp_too_humid`
    FROM setpoints
    WHERE `id` = 1
"""
pinsQuery = """
SELECT `id`, `pin`, `name`
FROM pins
"""

#Grab pin from db
db = MySQLdb.connect("localhost", "monitor", "raspberry", "temps")
curs = db.cursor()
with db:
   curs.execute (pinsQuery)
LIGHT = -1		#Relay1
FAN_CIRCULATE = -1	#Relay2
FAN_EMERGENCY = -1	#Relay3
FAN_HUMID = -1		#Relay4
for (id, pin, name) in curs:
    if (id == 1):
	LIGHT = int(pin)
    if (id == 2):
        FAN_CIRCULATE = int(pin)
    if (id == 3):
	FAN_EMERGENCY = int(pin)
    if (id == 4):
        FAN_HUMID = int(pin)
curs.close()
db.close()

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
    for (sp_high, sp_low, sp_too_hot, sp_high_h, sp_low_h, sp_too_humid) in curs:
        sp = (sp_high, sp_low, sp_too_hot, sp_high_h, sp_low_h, sp_too_humid)

    curs.close()
    db.close()

    return results, sp

def autoTemp():
    while(1):
        temp, sp = getData()
        tempC = float(temp[0])
        tempF = 9.0/5.0 * tempC + 32.0
        humid = float(temp[1])
        sp_high = float(sp[0])
        sp_low = float(sp[1])
        sp_too_hot = float(sp[2])
        sp_high_h = float(sp[3])
        sp_low_h = float(sp[4])
        sp_too_humid = float(sp[5])

        if (tempC > sp_high):
            #Turn Off Heater
            setPin(LIGHT, GPIO.IN)
        elif (tempC < sp_low):
            #Turn On Heater
            setPin(LIGHT, GPIO.OUT)

        if (tempC < sp_too_hot) and (humid < sp_too_humid):
            #Turn Off FAN_EMERGENCY
            setPin(FAN_EMERGENCY, GPIO.IN)
        elif (tempC >= sp_too_hot) or (humid > sp_too_humid):
            #Turn On FAN_EMERGENCY
            setPin(FAN_EMERGENCY, GPIO.OUT)

        if (humid > sp_high_h):
            #Turn OFF FAN_HUMID
            setPin(FAN_HUMID, GPIO.IN)
        elif (humid < sp_low_h):
            #Turn ON FAN_HUMID
            setPin(FAN_HUMID, GPIO.OUT)

        #Always have the circulation fan on
	setPin(FAN_CIRCULATE, GPIO.OUT)

        time.sleep(5)

if __name__ == "__main__":
    autoTemp()
