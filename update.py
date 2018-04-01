
from communication import Link
from time import sleep
import sys
import sqlite3

link = Link()

if len(sys.argv) < 3:
    print 'Usage: update.py <file.sqlite3> <delay>'
    sys.exit(1)

db = sqlite3.connect(sys.argv[1])

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

    print img

    sleep(int(sys.argv[2]))
