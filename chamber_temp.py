import serial
import string
import time
import sys
from optparse import OptionParser

def parse_input():
	parser = OptionParser()
	parser.add_option("-t", "--temp", dest="temp", help="Setting the Temperature of the VT4002 chamber")
	(options,args) = parser.parse_args()

	if options.temp == None or options.temp.strip()=="":
		print "Please provide valid temperature"
		sys.exit(-1)
	if float(options.temp) >= 66 or float(options.temp) <= -30 :
		print "Please provide temperature within the allowed range (-30 to +65)"
		sys.exit(-1)
	return options.temp

def set_temp(temp):
	# sets the temperature as temp 
	ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
	nominal_temp_string = "$00E "+ temp+"\r\n"
	ser.write(nominal_temp_string) 
	time.sleep(2)
	
	'''verifying by reading the present nominal temperature and
           compare it with the input temperature '''
	ser.write("$00I\r\n")
	line = ser.readline()
	value = string.split(line, ' ')
	if value[0] != "" and float(value[0]) == float(temp):
		print "Temperature set to "+ value[0] + " successfully"
	else:
		print "Error in setting temperature. Please check the setup"

if __name__=="__main__":
	temp = parse_input()
	try:
		set_temp(temp)
	except:
		print "Error in setting temperature. Please check the setup"
		  
