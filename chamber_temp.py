#! /usr/bin/python3

from optparse import OptionParser

#portname = '/dev/ttyS0'
portname = 'COM8'
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

def set_temp(temp):
	# sets the temperature as temp 
	ser = serial.Serial(portname, 9600, timeout=1)
	nominal_temp_string = '${:02X}E {}\r\n'.format(address,temp)
	ser.write(nominal_temp_string.encode('ascii')) 
	#time.sleep(2)
	
	'''verifying by reading the present nominal temperature and
	   compare it with the input temperature '''
	ser.write('${:02X}I\r\n'.format(address).encode('ascii'))
	lines = ser.readlines()
	#print(lines)
	line=lines[len(lines)-1].decode('ascii')
	value = line.split(' ')
	value = value[0].split('\r')
	#print(value)
	if len(value)>1 and value[1]!='' and float(value[1])==float(temp):
		print('Temperature set to {} successfully'.format(temp))
	else:
		print('Error in setting temperature. Please check the setup')

if __name__=="__main__":
	#temp = parse_input()
	temp=35.0
	try:
		set_temp(temp)
	except:
		print('Error in setting temperature. Please check the setup')
		  

