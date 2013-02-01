#! /usr/bin/python3

import serial
from optparse import OptionParser

#portname = '/dev/ttyS0'
portname = 'COM8'
timeout = 0.5
address = 1

def parse_input():
	parser = OptionParser()
	parser.add_option("-t", "--temp", dest="temp", help="Setting the Temperature of the VT4002 chamber")
	(options,args) = parser.parse_args()

	if options.temp == None or options.temp.strip()=="":
		print("Please provide valid temperature")
		sys.exit(-1)
	if float(options.temp) >= 66 or float(options.temp) <= -30 :
		print("Please provide temperature within the allowed range (-30 to +65)")
		sys.exit(-1)
	return options.temp

def set_temp(temp,status=None):
	# sets the temperature as temp 
	ser = serial.Serial(portname, 9600, timeout=timeout)
	if status=='start':
		nominal_temp_string = '${:02X}E {:4.1f} 80.0 27.5 0.0 27.0 -191.3 0.0 -191.3 25.5 -191.3 0111000000000000\r\n'.format(address,temp)
	elif status=='stop':
		nominal_temp_string = '${:02X}E {:4.1f} 80.0 27.5 0.0 27.0 -191.3 0.0 -191.3 25.5 -191.3 0000000000000000\r\n'.format(address,temp)
	else:
		nominal_temp_string = '${:02X}E {:4.1f}\r\n'.format(address,temp)
	#print(nominal_temp_string)
	ser.write(nominal_temp_string.encode('ascii'))
	ser.readlines() #flush port (ack should be there)
	
	'''verifying by reading the present nominal temperature and
	   compare it with the input temperature '''
	ser.write('${:02X}I\r\n'.format(address).encode('ascii'))
	lines = ser.readlines()
	line=lines[len(lines)-1].decode('ascii')
	value = line.split(' ')
	#print(value)
	if len(value)>0 and value[0]!='' and float(value[0])==float(temp):
		print('Temperature set to {} successfully'.format(temp))
	else:
		print('Error in setting temperature. Please check the setup')

if __name__=="__main__":
	'''temp = parse_input()
	try:
                set_temp(temp)
	except:
		print('Error in setting temperature. Please check the setup')
	'''
	#set_temp(35.0)
	#set_temp(35.0,'start')
	set_temp(35.0,'stop')
		  

