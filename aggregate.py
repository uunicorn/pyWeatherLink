
import sqlite3
import math
import sys

if len(sys.argv) < 4:
    print "Usage: aggregate.py <from.sqlite3> <to.sqlite3> <-5 minute>"
    sys.exit(1)

db = sqlite3.connect(sys.argv[1])

class WindAvg:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.n = 0

    def step(self, direction, speed):
        self.x = self.x + speed*math.sin(math.radians(direction))
        self.y = self.y + speed*math.cos(math.radians(direction))
        self.n = self.n + 1

    def avg_x(self):
        return self.x / self.n

    def avg_y(self):
        return self.y / self.n

    def speed(self):
        return math.sqrt(math.pow(self.avg_x(), 2) + math.pow(self.avg_y(), 2))

    def direction(self):
        return math.degrees(math.atan2(self.avg_x(), self.avg_y()))

class WindAvgSpeed(WindAvg):
    def finalize(self):
        return self.speed()

class WindAvgDirection(WindAvg):
    def finalize(self):
        if self.speed() > 0:
            return self.direction()
        else:
            return 0


db.create_aggregate('WindAvgSpeed', 2, WindAvgSpeed)
db.create_aggregate('WindAvgDirection', 2, WindAvgDirection)

sql="""
select max(timestamp), 
    max(WindSpeed),
    WindAvgSpeed(WindDirection, AverageWindSpeed),
    WindAvgDirection(WindDirection, AverageWindSpeed),
    avg(IndoorTemperature),
    avg(IndoorRelativeHumidity),
    avg(OutdoorTemperature),
    avg(OutdoorRelativeHumidity),
    avg(QFE),
    avg(RainRate),
    max(RainDay),
    avg(OutdoorDewpoint)
from image where timestamp > datetime('now', ?)
"""

result = db.cursor().execute(sql, (sys.argv[3],)).fetchone()
print result

db.close()

db = sqlite3.connect(sys.argv[2])
sql="""
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
    OutdoorDewpoint
) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
db.cursor().execute(sql, result);
db.commit()
db.close()

