#!/usr/bin/python
import threading
import serial
import sliplib
import OSC
from Queue import Queue
from time import sleep

port = '/dev/ttyS1'
baud = 115200
#baud = 921600
_timeout = .1 #115200/8 = 14400 bytes/sec,
#largest send is 128 bytes MAYBE
#0.00006944444 sec/byte
#timeout of .088
driver=sliplib.Driver()
'''
def slipD(bytes):
	return driver.receive(bytes)
	
def slipE(string):
	return driver.send(string)

def OSCdecode(string):
	if string != []:
		str = ''.join(string) #byte array to actual string
		return OSC.decode(str)
	else:
		return 0

def OSCencode(string):
	return OSC.encode(string)

def readSerial(serial):
	line = serial.readline()
	return OSCencode(slipD(line))

def sendSerial(serial,string):
	serial.write(OSCencode(slipE(string)))

serial_port = serial.Serial(port, baud, timeout=_timeout)
cham=Queue()

def handle_data(data):
	print(data)
'''

cham = Queue()
serial_port = serial.Serial(port, baud,timeout=_timeout)

def read_from_port(ser,q):
	while True:
		reading = ser.readline()
		try:
			halfd= driver.receive(reading)
			str = ''.join(halfd)
			if halfd != []:
				print OSC.decodeOSC(str)
				q.put(OSC.decodeOSC(str))
		except:
			print "malformed OSC packet"
			print reading
'''
def print_from_port(q):
	while True:
		a = q.get()
		print a
		sleep(.2)
'''
thread1 = threading.Thread(target=read_from_port, args=(serial_port,cham,))
#thread2 = threading.Thread(target=print_from_port, args=(cham,))
thread1.start()
#thread2.start()

