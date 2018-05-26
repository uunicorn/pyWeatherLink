#!/bin/bash
# add to crontab:
# */5 * * * * /root/pyWeatherLink/aggregate.sh


TEMP=/tmp/weather
PERSISTENT=/var/local/weather
RAW="$TEMP/raw.sqlite3"
AGG5MIN="$PERSISTENT/5min_avg.sqlite3"
PYLINK=/root/pyWeatherLink

cd "$PYLINK"

exec >> aggregate.log 2>&1

test -f "$RAW" || exit 0

mkdir -p "$PERSISTENT"

test -f "$AGG5MIN" || sqlite3 "$AGG5MIN" < schema.sql

time python aggregate.py "$RAW" "$AGG5MIN" '-5 minute'

time python render-report.py "$AGG5MIN" "$TEMP/report.png"

cd rose

python render-rose.py "$AGG5MIN" "$TEMP/rose.png" '-1 hour'

cd $TEMP

TS="strftime('%Y-%m-%dT%H:%M:%S', timestamp)"
FROM="from image where timestamp > datetime('now', '-1 day')"

sqlite3 -separator ' ' -nullvalue '?' "$AGG5MIN" \
    "select $TS,                    -- 1
        OutdoorTemperature,         -- 2
        OutdoorDewpoint,            -- 3
        OutdoorRelativeHumidity,    -- 4

        AverageWindSpeed,           -- 5
        WindDirection,              -- 6
        WindSpeed,                  -- 7

        RainRate,                   -- 8
        RainDay,                    -- 9

        QFE                         -- 10
    $FROM" > plot.dat

gnuplot "$PYLINK/plot.cmd"
