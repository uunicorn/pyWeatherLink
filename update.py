
from communication import Link
from time import sleep, strftime, gmtime
from urllib import urlencode
import wunderground
import sys
import os
import sqlite3

if len(sys.argv) < 3:
    print 'Usage: update.py <file.sqlite3> <delay>'
    sys.exit(1)

interval = int(sys.argv[2])

db = sqlite3.connect(sys.argv[1])

link = Link()

while True:
    img=link.getSensorImage()
    c=db.cursor()
    c.execute("""
insert into image (
    timestamp, 
    WindSpeed, 
    AverageWindSpeed,
    WindDirection,
    IndoorTemperature,
    IndoorRelativeHumidity,
    OutdoorTemperature,
    OutdoorRelativeHumidity,
    QFE,
    RainRate,
    RainDay,
    OutdoorDewpoint) 
values (datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", 
    (img.WindSpeed, 
    img.AverageWindSpeed,
    img.WindDirection,
    img.IndoorTemperature,
    img.IndoorRelativeHumidity,
    img.OutdoorTemperature,
    img.OutdoorRelativeHumidity,
    img.QFE,
    img.RainRate,
    img.RainDay,
    img.OutdoorDewpoint)) 
    db.commit()

    params=urlencode({
        'ID': wunderground.stationid,
        'PASSWORD': wunderground.password,
        'dateutc': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        'winddir': img.WindDirection,
        'windspeedmph': img.AverageWindSpeedMPH,
        'windgustmph': img.WindSpeedMPH,
        'tempf': img.OutdoorTemperatureF,
        'rainin': img.RainRate,
        'baromin': img.QFEInHg,
        'humidity': img.OutdoorRelativeHumidity,
        'softwaretype': 'pyWeatherLink v0.0',
        'action': 'updateraw',
        'realtime': 1,
        'rtfreq': interval
    })
    url='https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?' + params
    
    os.system('curl --silent "' + url + '" &')

    sleep(interval)
