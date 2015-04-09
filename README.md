# raspi-incubator
Incubator using a Raspberry Pi with temperature/humidity sensor(s) and heat control using a light and fan on relays.
Using the Raspberry Pi as a web server, an incubator can be monitored and controlled through a web interface.  Additionally, a webcam could be used for remote monitoring if desired.

## Equipment
- [8GB micro sd card](https://www.amazon.com/gp/product/B00200K1TS/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
- [DHT11 humidity/temperature sensor](https://www.amazon.com/gp/product/B007YE0SB6/ref=od_aui_detailpages00?ie=UTF8&psc=1)
- Dallas DS18b20 temperature sensor (for initial testing while the others are on their way)
- [Raspberry Pi model B+](http://www.amazon.com/gp/product/B00LPESRUK/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
- [Edimax Wi-Fi USB adapter](https://www.amazon.com/gp/product/B003MTTJOY/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)
- [Sainsmart 4-channel relay module](https://www.amazon.com/gp/product/B0057OC5O8/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1)

## Initial Setup

- Install the [latest Raspbian Wheezy image](http://www.raspberrypi.org/downloads/) (Kernel version 3.18, Release 2015-02-16 at the time of this writing).
- Perform whatever your prefered setup within raspi-config (expand filesystem, enable ssh, etc...)
- Enable network access by generating a wpa passphrase for your network
```
wpa_passphrase <netowork SSID>
```
- Copy the output of this to ```/etc/wpa_supplicant/wpa_supplicant.conf``` and add ```id_str="home"```
- Restart Raspberry pi then run the following commands:
```
sudo apt-get update
sudo apt-get upgrade
```
- Install Flask and httplib2
```
sudo apt-get install python-pip -y
sudo pip install flask
sudo pip install httplib2
```
### MySQL Database Setup
- Install MySQL database and create the database and user
```
sudo apt-get install mysql-server python-mysqldb -y
mysql -u root -p
mysql> CREATE DATABASE temps;
mysql> USE temps
mysql> CREATE USER 'monitor'@'localhost' IDENTIFIED BY 'raspberry';
mysql> GRANT ALL PRIVILEGES ON temps.* TO 'monitor'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> quit
```
- Now, reenter the shell with the new user to create the table.
```
mysql -u monitor -p
mysql> USE temps
mysql> CREATE TABLE tempdat (tdate DATE, ttime TIME, zone TEXT, temperature NUMERIC, humidity NUMERIC);
mysql> quit
```
### Server Setup
Steps to setup the webserver manually.  I'm writing these as I try different things.  I found a great tutorial on using Flask and the raspberry pi [here](http://mattrichardson.com/Raspberry-Pi-Flask/) and [here](http://www.keithsterling.com/?p=493)

- Create a test file hello-flask.py
```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
```
- Now run the server
```sudo python hello-flask.py```
- Navigate to your ip address from another computer to verify that the server is up and running

### Wiring

## DHT11 Setup
[Adafruit's guide to setting up the DHT11](https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/overview).  
