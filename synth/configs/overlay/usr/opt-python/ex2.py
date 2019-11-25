#!/usr/bin/python
import threading
import serial
import sliplib
import OSC

#connected = False
port = '/dev/ttyS1'
baud = 115200
_timeout = .088 #115200/8 = 14400 bytes/sec,
#largest send is 128 bytes MAYBE
#0.00006944444 sec/byte
#timeout of .088
driver=sliplib.Driver()
serial_port = serial.Serial(port, baud, timeout=_timeout)

def handle_data(data):
    print(data)

def read_from_port(ser):
 #   while not connected:
        #serin = ser.read()
  #      connected = True

        while True:
#           print("test")
           reading = ser.readline()
 #          print OSC.decodeOSC(driver.receive(reading))
           try:
               halfd= driver.receive(reading)
               str = ''.join(halfd)
               if halfd != []:
                   print OSC.decodeOSC(str)
           except:
               print "malformed OSC packet"
               

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()
#import serial, sliplib
#com = serial.Serial('/dev/ttyS0',115200)
#driver = sliplib.Driver() 
#message = bytes("hello my friend")
#com.write(driver.send(message))
#serial_port.close()

