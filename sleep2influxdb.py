#/usr/bin/env python3
#
# sleep2influxdb.py
#
# store Sleep As Android csv data in influxdb
#
# author: Henrik Pingel
# email: knowhy@gmail.com
#
# license: MIT


import time
import csv
import json
from influxdb import InfluxDBClient
from datetime import datetime

influxdb_dbname = 'sleeptest'
influxdb_user = 'admin'
influxdb_password = 'admin'
influxdb_host = 'influxdb_host'
influxdb_port = '8086'

client = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_dbname)

with open('sleep.csv') as csvfile:
    sleep_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in sleep_reader:
        try:
            row_length = len(row[1])
            if row_length > 2:
                day = row[2].split().pop(0)
                month = row[2].split().pop(1)
                year = row[2].split().pop(2)
                time = row[2].split().pop(3)
                hour, minute = time.split(':')
                current_time = year + "-" + month[:-1] + "-" + day[1:-1] + "T" + hour + ":" + minute[0] + minute[1] + "SZ"
                sleepid = row[0]
                tz = row[1]
                sleepfrom = row[2]
                sleepto = row[3]
                sched = row[4]
                hours = row[5]
                rating = row[6]
                comment = row[7]
                framerate = row[8]
                snore = row[9]
                noise = row[10]
                cycles = row[11]
                deepsleep = row[12]
                lenadjust = row[13]
                geo = row[14]
                json_body = [
                    {
                        "measurement": "sleep",
                        "tags": {
                            "sensor": "sleep"
                        },
                        "time": current_time,
                        "fields": {
                            "id": sleepid[1:-1],
                            "tz": tz[1:-1],
                            "from": sleepfrom[1:-1],
                            "to": sleepto[1:-1],
                            "sched": sched[1:-1],
                            "hours": float(hours[1:-1]),
                            "rating": float(rating[1:-1]),
                            "comment": comment[1:-1],
                            "framerate": framerate[1:-1],
                            "snore": float(snore[1:-1]),
                            "noise": float(noise[1:-1]),
                            "cycles": float(cycles[1:-1]),
                            "deepsleep": float(deepsleep[1:-1]),
                            "lenadjust": float(lenadjust[1:-1]),
                            "geo": geo[1:-1]
                        }
                    }
                ]
                client.write_points(json_body)
        except:
            continue
