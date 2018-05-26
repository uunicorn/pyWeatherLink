from MakeText import make_text
import sqlite3
import sys
from time import asctime, gmtime
import os

report='/tmp/weather/report.png'

if len(sys.argv) < 3:
    print 'Usage: render-report.py <file.sqlite3> <file.png>'
    sys.exit(1)

db = sqlite3.connect(sys.argv[1])

sql="""
select OutdoorTemperature, OutdoorRelativeHumidity, AverageWindSpeed, WindDirection, WindSpeed, QFE
from image 
order by timestamp desc
"""
result = db.cursor().execute(sql).fetchone()

print result

txt='''\
%s UTC
Temperature %s C
Humidity %s %%
Wind %s knots @ %s
Gusting %s knots
QNH %s
'''

def f(fmt, val):
    if val == None:
        return None
    else:
        return fmt % val

txt = txt % (
    asctime(gmtime()), 
    f("%.1f", result[0]), 
    f("%.0f", result[1]),
    f("%.1f", result[2]), f("%03d", result[3]),
    f("%.1f", result[4]), 
    f("%.1f", result[5])
)

make_text(txt).save(report + '.new.png')
os.rename(report + '.new.png', report)
