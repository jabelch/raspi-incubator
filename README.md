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

## Setup

- Install the [latest Raspbian Wheezy image](http://www.raspberrypi.org/downloads/) (Kernel version 3.18, Release 2015-02-16 at the time of this writing).
- Perform whatever your prefered setup within raspi-config (expand filesystem, enable ssh, etc...)
- Run the following commands:
```
sudo apt-get update
sudo apt-get upgrade
```
### Manual Setup
Steps to setup the webserver manually.  I'm writing these as I try different things.  I found a great tutorial on using Flask and the raspberry pi [here](http://mattrichardson.com/Raspberry-Pi-Flask/)
- Install Flask
```
sudo apt-get install python-pip
sudo pip install flask
```
- Create a test file hello-flask.py
```
from Flask import Flask
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
