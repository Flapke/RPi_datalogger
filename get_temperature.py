#!/usr/bin/env python3

import time
import csv
import datetime
import sqlite3
from w1thermsensor import W1ThermSensor, Sensor

sensors = [];
data = [];

with open('./data/temp_sensors.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    for item in list(reader):
        sensors.append(item[0]);
readFile.close();

def get_temperatures():
    data.clear();
    i = 1;
    for item in sensors:
        timestamp = datetime.datetime.now();
        sensor = W1ThermSensor(Sensor.DS18B20, item);
        temperature = sensor.get_temperature();
        print("%s Sensor %s has temperature %.2f" % (timestamp, i, temperature));
        data.append([timestamp, i, temperature]);
        i = i + 1;

def save_dataCSV():
    filename = './data/tmp_' + datetime.datetime.now().strftime("%Y%m%d") + '.csv';
    with open(filename, 'a') as writeFile:
        writer = csv.writer(writeFile)
        for row in data:
            writer.writerow(row)
    writeFile.close();
    
def save_dataDB():
    db = sqlite3.connect('./data/db');
    cursor = db.cursor();
    cursor.executemany('INSERT INTO temperature VALUES (?,?,?)', data);
    db.commit();
    db.close();

#while True:
get_temperatures();
save_dataCSV();
save_dataDB();
    #time.sleep(60);
    
    
    