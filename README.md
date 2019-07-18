# A simple weather station kiosk

This setup is only intended to work with Davis weather station.


## How to configure

Following assumes that you have the sources under /root/pyWeatherLink

### What's need to be installed

* gnuplot
* python
* sqlite3
* ImageMagic's "convert" utility
* tvservice


### Directories with data

* /tmp/weather - temporary storage (will be updated at least once every 40 seconds and all the temporaty images are going to be kept there. Best if it's on a tmpfs so it won't kill the SD card too quickly)
* /var/local/weather - this is where the 5 min averages are going to be stored.

### inittab
```
T0:23:respawn:/root/pyWeatherLink/update.sh
```
This deamon will pull data from the Davis wx station, store them in a temporary sql database and push updates to the WeatherUnderground.

### crontab
This will render all images once every 5 minutes and drop them in /tmp/weather:
```
*/5 * * * * /root/pyWeatherLink/aggregate.sh
```

Turn the TV screen off at 22:00 and then back on at 05:00
```
0  22 * * * tvservice -o > /root/off.log 2>&1
0   5 * * * (tvservice -p; killall fbi) > /root/on.log 2>&1
```

Take a webcam shot once every 5 minutes. 
```
*/5 * * * * (cd /var/local/webcam/ && ./snap.sh) > /root/webcam.log 2>&1
```
The snap.sh and the rest of webcam-related scripts are not a part of this project, but I'm happy to share them on request.

### Set the WeatherUnderground credentials
In this directory create a file called `wunderground.py`:
```
stationid='XXXXX'
password='YYYYY'
```

### Integrating with a Web server

Pick up a location exposed by the web server and create bunch of sym-links to the images:
```
24hrs_full_features.png -> /tmp/weather/24hrs_full_features.png
dashboard.png -> /tmp/weather/dashboard.png
report.png -> /tmp/weather/report.png
rose.png -> /tmp/weather/rose.png
```
Create an html file with these images, e.g:
```
<html>
    <head>
        <title>RT Weather</title>
    </head>
    <body>
        <h1>Latest WebCam</h1>
        <a href="../webcam/"><img src="../webcam/latest.jpg"></a>
        <h1>Latest 5 minutes average</h1>
        <img src="report.png">
        <h1>Winds past 60 min</h1>
        <img src="rose.png">
        <h1>Weather past 24 hours</h1>
        <img src="24hrs_full_features.png">
    </body>
</html>
```

