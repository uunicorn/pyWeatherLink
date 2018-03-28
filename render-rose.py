
import sqlite3
import sys

if len(sys.argv) < 4:
    print 'Usage: render-rose.py <file.sqlite3> <file.png> <points>'
    sys.exit(1)

db = sqlite3.connect(sys.argv[1])

sql='select WindDirection, AverageWindSpeed from image order by timestamp desc'
result = db.cursor().execute(sql).fetchmany(int(sys.argv[3]))

print result

from rose import Rose

r=Rose()
r.rose(result)
r.im.save(sys.argv[2])
