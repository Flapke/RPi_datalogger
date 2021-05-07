#!/usr/bin/env python3

import os
import csv
from w1thermsensor import W1ThermSensor


def get_sensors(sensor_log):
    sensors = [];
    
    # Get the ids of all temperature sensors connected and set their precision to 12 bit
    for sensor in W1ThermSensor.get_available_sensors():
        sensors.append(sensor.id);
        sensor.set_resolution(12);
        
    # Write sensor ids to a file (reorder these as needed later)
    with open('./data/temp_sensors.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        for item in sensors:
            print("DS18B20 sensor found: " + item);
            writer.writerow([item,])
    
    writeFile.close()

def main():
    sensor_file = './data/temp_sensors.csv'
    if os.path.isfile(sensor_file):
        print("Sensor list available, skipping scan")
    else:
        get_sensors(sensor_file)
    


if __name__=="__main__":
    main()