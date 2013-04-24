#! /usr/bin/python3

import serial
import sys
from optparse import OptionParser


#default_portname = '/dev/ttyS0'
default_portname = 'COM3'
timeout = 0.5
#address = 0
address = 1


def parse_input():
	''' function parses input arguments
	it is used when works as the standalone module
	returns: [portname,temval,statusstr]
		portname (string) [default see definitions]
		tempval (float) [default None]
		statusstr (string) [default ON] '''
	
	parser = OptionParser()
	parser.add_option("-p", dest="port", help="VT4002 chamber serial port (default {})".format(default_portname))
	parser.add_option("-t", dest="temp", help="Setting the Temperature of the VT4002 chamber")
	parser.add_option("-s", dest="status", help="Setting the ON/OFF status of the VT4002 chamber (default ON)")
	(options,args) = parser.parse_args()

	portname = default_portname
	if options.port != None:
		portname = str(options.port)

	tempval = None
	if options.temp != None:
		if float(options.temp) >= 150 or float(options.temp) <= -50 :
			print("Please provide temperature within the allowed range (-50 to +150)")
			sys.exit(-1)
		else:
			tempval = float(options.temp)

	statusstr = None
	if options.status != None:
		statusstr = str(options.status)
		
	return [portname,tempval,statusstr]


def set_temp(portname,temp,status='ON',verbose=True):
	''' function sets final temperature and status of VT4002 chamber
	params: portname .. serial port name (string)
		temp .. final temperature (float)
		status .. chamber status (string .. ON / OFF) [default ON]
		verbose .. if True than verbose text output else return function [default True]
	returns (if verbose!=True):
		[final temperature (float), status (string)] if success
		'ERROR' if error '''
	
	ser = serial.Serial(portname, 9600, timeout=timeout)
	
	temp = temp
	if temp==None:
		temp=0.0

	tempstr = '0000.0'
	if temp<0:
		tempstr='-000.0'
	tstr = '{:4.1f}'.format(abs(temp))
	tempstr='{}{}'.format(tempstr[0:len(tempstr)-len(tstr)],tstr)
	if (status=='ON') or (status==None):
		nominal_temp_string = '${:02X}E {} 0080.0 0027.5 0000.0 0027.0 -191.3 0000.0 -191.3 0025.5 -191.3 0111000000000000\r\n'.format(address,tempstr)
	else:
		#note that this will stop the air conditioning
		nominal_temp_string = '${:02X}E {}\r\n'.format(address,tempstr)
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
		if verbose==True:
			print('Temperature set to {} successfully'.format(temp))
			print('Air conditioning is {}'.format('stopped' if value[10][1]=='0' else 'running'))
		else:
			return([temp,'OFF' if value[10][1]=='0' else 'ON'])
	else:
		if verbose==True:
			print('Error in setting temperature. Please check the setup')
		else:
			return('ERROR')


def read_temp(portname,verbose=True):
	''' function reads setted and actual temperature and status from VT4002 chamber
	params: portname .. serial port name
		verbose .. if True than verbose text output, else return function (default True)
	returns (if not verbose==True):
		[setted temperature (float), actual temperature (float), status (string)] if success
		'ERROR' string if error '''
	
	ser = serial.Serial(portname, 9600, timeout=1)
	ser.write('${:02X}I\r\n'.format(address).encode('ascii'))
	lines = ser.readlines()
	#print(lines)
	try:
		line = lines[len(lines)-1].decode('ascii')
		value = line.split(' ')
		#print(value)
		stemp = float(value[0])
		atemp = float(value[1])
		if verbose==True:
			print('Set at Temperature: {}C'.format(stemp))
			print('Actual Temperature: {}C'.format(atemp))
			print('Air conditioning is {}'.format('stopped' if value[10][1]=='0' else 'running'))
		else:
			return([stemp,atemp,'OFF' if value[10][1]=='0' else 'ON'])
		
	except:
		if verbose==True:
			print('Can\'t get correct feedback!')
		else:
			return('ERROR')

		
if __name__=="__main__":
	[port,temp,status] = parse_input()
	#print([port,temp,status])
	try:
		if temp!=None or status!=None:
			set_temp(port,temp,status)
		else:
			read_temp(port)
	except:
		print('Error in setting/reading temperature. Please check the setup.')
