#!/usr/bin/python
import serial
import sliplib
import OSC
def serial_data(port, baudrate):
	ser = serial.Serial(port, baudrate)
	while True:
		ser.write([192,47,103,101,116,107,110,111,98,115,0,0,0,44,0,0,0,192]) #/getknobs OSC/slipenc
		bytesToRead=ser.inWaiting()
		if bytesToRead != 0:
			yield ser.read(bytesToRead)
	ser.close()

driver=sliplib.Driver()

for line in serial_data('/dev/ttyS1', 921600):
#	half=driver.receive(line)
	print OSC.decodeOSC(''.join(driver.receive(line)))
