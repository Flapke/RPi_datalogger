#!/usr/bin/env python3

import os
import csv
import datetime
from w1thermsensor import W1ThermSensor


def write_sensor_list(sensor_log):
    sensors = []
    
    # Get the ids of all temperature sensors connected and set their precision to 12 bit
    for sensor in W1ThermSensor.get_available_sensors():
        sensors.append(sensor.id)
        sensor.set_resolution(12)
        
    # Write sensor ids to a file (reorder these as needed later)
    with open('./data/temp_sensors.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        for item in sensors:
            writer.writerow([item,])
    
    writeFile.close()
    
    print("DS18B20 sensors found: " + sensors)


def read_sensor_list(sensor_log):
    sensors = []
    with open(sensor_log, 'r') as readFile:
        reader = csv.reader(readFile)
        for item in list(reader):
            sensors.append(item[0])
    readFile.close()
    return sensors


def get_temperatures(sensors):
    data = []
    i = 0
    for item in sensors:
        timestamp = datetime.datetime.now()
        sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, item)
        temperature = sensor.get_temperature()
        print("Sensor %s: %.2f degC" % (i, temperature))
        data.append([timestamp, i, temperature])
        i = i + 1
    return data


def main():
    sensor_file = './data/temp_sensors.csv'
    if os.path.isfile(sensor_file):
        print("Sensor list available, skipping scan")
    else:
        write_sensor_list(sensor_file)
    sensors = read_sensor_list(sensor_file)
    get_temperatures(sensors)
    

if __name__=="__main__":
    main()
    
    
    
    