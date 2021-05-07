#!/usr/bin/env python3

import time
import csv
import logging
import thingspeak
import minimalmodbus
from w1thermsensor import W1ThermSensor

channel = thingspeak.Channel(id=1045583, api_key='PMSG82Y1NL3ZL3HT')

pyranometer = minimalmodbus.Instrument('/dev/ttyUSB0', 1, minimalmodbus.MODE_RTU)
pyranometer.serial.baudrate = 19200
pyranometer.serial.bytesize = 8
pyranometer.serial.parity =  'E'
pyranometer.serial.stopbits = 1

sensors = []
data = []

logging.basicConfig(filename = './data/error_log.csv', level=logging.WARNING)


with open('./data/temp_sensors.csv', 'r') as readFile:
    reader = csv.reader(readFile)
    for item in list(reader):
        sensors.append(item[0])
readFile.close()


def getTemperature():
    data.clear()
    i = 0
    for item in sensors:
        sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, item)
        temperature = sensor.get_temperature()
        print("Sensor %s: %.2f degC" % (i, temperature))
        data.append(temperature)
        i = i + 1


def getIrradiance():
    # Register number, function code, signed
    irradiance = pyranometer.read_long(2, 3, True)/100
    # Register number, number of decimals, function code, signed
    temperature = pyranometer.read_register(6, 2, 3, True)
    print("Irr: " + str(irradiance) + " W/m2 Temp: " + str(temperature) + " degC")
    return(irradiance)


def sendData(channel, temp1, temp2, irr):
    try:
        response = channel.update({'field1': temp1, 'field2': temp2, 'field3' : irr})
        #read = channel.get({})
        #print("Read:", read)
        
    except:
        print("Connection failed")
        
def pollApi(self, tries, initial_delay, delay, backoff, success_list, apifunction, *args):
    time.sleep(initial_delay)
    for n in range(tries):
        try:
            status = self.get_status()
            if status not in success_list:
                polling_time = time.strftime("%a, %d %b %Y %H:%H:%S", time.localtime())
                print("{0}. Sleeping for {1} seconds".format(polling_time, delay))
                time.sleep(delay)
                delay *= backoff
            else:
                return apifunction(*args)
        except socket.error as e:
            print("Connection dropped with error code {0}".format(e.errno))
    raise ExceededRetries("Failed to poll {0} within {1} tries.".format(apifunction, tries))


def main():
    
    global channel
    
    while True:
        tries = 10
        delay = 1
        backoff = 2
        for n in range(tries):
            try:
                getTemperature()
                temp1 = data[0]
                temp2 = data[1]
                irr = getIrradiance()
                sendData(channel, temp1, temp2, irr)
                time.sleep(1)
                break
            except Exception as e:
                logging.exception(e)
                print(e)
                time.sleep(delay)
                delay *= backoff
                pass
            if n is tries-1:
                raise Exception("Failed after {0} tries.".format(tries))

if __name__=="__main__":
    main()
   
   
   