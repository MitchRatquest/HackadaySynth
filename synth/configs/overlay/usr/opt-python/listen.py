#!/usr/bin/python
import socket
import OSC

localhost = "127.0.0.1"
listenport = 4001

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((localhost, listenport))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print OSC.decodeOSC(data.strip("\n").strip(";"))

