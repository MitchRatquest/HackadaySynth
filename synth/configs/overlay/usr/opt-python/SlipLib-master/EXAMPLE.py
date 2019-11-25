#!/usr/bin/python
import serial, sliplib
com = serial.Serial('/dev/ttyS0',115200)
driver = sliplib.Driver() 
message = bytes("hello my friend")
com.write(driver.send(message))
com.close()
