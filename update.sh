#!/bin/sh

# add to inittab:
# T0:23:respawn:/root/pyWeatherLink/update.sh


WORKDIR="/tmp/weather"
RAW="$WORKDIR/raw.sqlite3"

cd /root/pyWeatherLink

exec >> update.log 2>&1

mkdir -p "$WORKDIR"

test -f "$RAW" || sqlite3 "$RAW" < schema.sql

python update.py "$RAW" 10
