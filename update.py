
from communication import Link
from time import sleep
import sqlite3

link = Link()

db = sqlite3.connect('raw.sqlite3')

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

    sleep(10)
