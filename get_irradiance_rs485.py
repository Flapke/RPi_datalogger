#!/usr/bin/env python3
import minimalmodbus
import csv
import time
import datetime
import sqlite3
import numpy as np
import pandas as pd

# port name, slave address (in decimal)
pyranometer = minimalmodbus.Instrument('/dev/ttyUSB0', 1, minimalmodbus.MODE_RTU);
pyranometer.serial.baudrate = 19200;
pyranometer.serial.bytesize = 8;
pyranometer.serial.parity = 'E';
pyranometer.serial.stopbits = 1;

average_time = 60;

data = [];

def get_irradiance():
    timestamp = datetime.datetime.now();
    # Register number, function code, signed
    irradiance = pyranometer.read_long(2, 3, True)/100
    # Register number, number of decimals, function code, signed
    temperature = pyranometer.read_register(6, 2, 3, True)
    print("Irr: " + str(irradiance) + "W/m2 Temp: " + str(temperature) + "degC")
    return([timestamp, irradiance]);

def average_data(data):
    df = pd.DataFrame(data);
    print(df);
    return([timestamp, irradiance]);

def save_dataCSV(data):
    filename = '/usr/share/adafruit/webide/repositories/my-pi-projects/data_logger/data/irr_' + datetime.datetime.now().strftime("%Y%m%d") + '.csv';
    with open(filename, 'a') as writeFile:
        writer = csv.writer(writeFile)
        for row in data:
            writer.writerow(row)
    writeFile.close();
    
def save_dataDB(data):
    db = sqlite3.connect('/usr/share/adafruit/webide/repositories/my-pi-projects/data_logger/data/db');
    cursor = db.cursor();
    cursor.executemany('INSERT INTO irradiance VALUES (?,?)', data);
    db.commit();
    db.close();

#while True:
    #start_time = time.time();
    #while(time.time()-start_time < average_time):
data.append(get_irradiance());
save_dataCSV(data);
save_dataDB(data);
    #save_dataCSV(average_data(data));
    #save_dataDB(average_data(data));
    #data.clear();
    #time.sleep(60);
    
    
    