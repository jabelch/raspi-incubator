import MySQLdb

#High and Low set points (fahrenheit)
SP_HIGH = 100
SP_LOW = 95

class Incubator:
    Heating = 1
    Cooling = 2
    sp_high = 100
    sp_low = 95

selectQuery = """
    SELECT `temperature`, `humidity`
    FROM tempdat
    ORDER BY `tdate` DESC, `ttime` DESC
    LIMIT 1
"""

def getTemp():
    #Grab the latest reading from database
    db = MySQLdb.connect("localhost", "monitor", "raspberry", "temps")
    curs=db.cursor()

    with db:
        curs.execute (selectQuery)
    results = []
    for (temperature, humidity) in curs:
        results.append([temperature, humidity])

    curse.close()
    db.close()

    return results

def autoTemp():
    while(1)
        reading = getTemp()
        
