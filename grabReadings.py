#!/usr/bin/python

import Adafruit_DHT
import MySQLdb
import sys
import time
import datetime

#Location, User, Password, DB
db = MySQLdb.connect("localhost", "monitor", "raspberry", "temps")
db.autocommit(True)
curs = db.cursor()

# zone, pin, sensortype
sensor = ['dht01', 2, Adafruit_DHT.DHT11]

# How long to wait (in seconds) between measurements
FREQ_MEASURE = 10

print 'Logging temp/humidity to MySQL database every {0} seconds.'.format(FREQ_MEASURE)
while True:
	# Attempt to get sensor reading.
	humidity, temp = Adafruit_DHT.read(sensor[2], sensor[1])

	if humidity is None or temp is None:
		continue

	temp = '{0:0.1f}'.format(temp)
	humidity = '{0:0.1f}'.format(humidity)
	#print str(temp) + " " + str(humidity) + "\n"

	insertQuery = """
		INSERT INTO tempdat
		(`tdate`, `ttime`, `zone`, `temperature`, `humidity`)
		VALUES
		(CURRENT_DATE(), NOW(), 'th', %s, %s)
		"""
        deleteQuery = """
                DELETE FROM tempdat
                WHERE `tdate` < DATE_SUB(NOW(), INTERVAL 2 DAY)
                """
	with db:
		curs.execute(insertQuery, (temp, humidity))
                curs.execute(deleteQuery)

	# Wait specified time between readings
	time.sleep(FREQ_MEASURE)


db.close()
