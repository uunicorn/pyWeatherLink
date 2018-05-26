
import sqlite3
import sys

if len(sys.argv) < 4:
    print 'Usage: render-rose.py <file.sqlite3> <file.png> <-1 hour>'
    sys.exit(1)

db = sqlite3.connect(sys.argv[1])

sql="""
select WindDirection, AverageWindSpeed 
from image 
where timestamp > datetime('now', ?) 
order by timestamp asc
"""
result = db.cursor().execute(sql, (sys.argv[3],)).fetchall()

#print result

from rose import Rose

r=Rose()
r.rose(result)
r.im.save(sys.argv[2])
