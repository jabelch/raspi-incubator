#RESTful Server using Flask
from flask import Flask, request, json
import MySQLdb

db = MySQLdb.connect("localhost", "monitor", "raspberry", "temps")
curs=db.cursor()

#Grab temperature and humidity data
curTemp = 20.0;
curHumid = 20;

#Insert data into database
with db:
    curs.execute ("""INSERT INTO tempdat 
            values(CURRENT_DATE(), NOW(), 'eggs', curTemp, curHumid)""")

#Grab data from database
curs.execute ("SELECT * FROM tempdat WHERE tdate>%s", % str(CURRENT_DATE() - INTERVAL 1 DAY))
