#! /usr/bin/python3

import serial

#portname = '/dev/ttyS0'
portname = 'COM8'
address = 1

ser = serial.Serial(portname, 9600, timeout=1)
ser.write('${:02X}I\r\n'.format(address).encode('ascii'))
lines = ser.readlines()
try:
        line = lines[len(lines)-1].decode('ascii')
        value = line.split(' ')
        print(value)
        stemp = float(value[0])
        atemp = float(value[1])
        print('Set at Temperature: {}C'.format(stemp))
        print('Actual Temperature: {}C'.format(atemp))
except:
        print('Can\'t get correct feedback!')
