import serial
import string
import time

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
while True:
	ser.write("$00I\r\n")
	line = ser.readline()
	value = string.split(line, ' ')
	print "============================================"
	print "Set at Temperature: "+ value[0] + " C"
	print "Actual Temperature: "+ value[1] + " C"
	time.sleep(2)
print "============================================"
