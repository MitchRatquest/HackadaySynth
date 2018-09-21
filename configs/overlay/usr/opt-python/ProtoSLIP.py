import termios
import serial
from collections import deque

# declared in octal  
SLIP_END = 0300
SLIP_ESC = 0333
SLIP_ESC_END = 0334
SLIP_ESC_ESC = 0335
DEBUG_MAKER = 0015
MAX_MTU = 200
readBufferQueue = deque([])

# This function takes a byte list, encode it in SLIP protocol and return the encoded byte list  
def encodeToSLIP(byteList):
    tempSLIPBuffer = []
    tempSLIPBuffer.append(SLIP_END)
    for i in byteList:
        if i == SLIP_END:
            tempSLIPBuffer.append(SLIP_ESC)
            tempSLIPBuffer.append(SLIP_ESC_END)
        elif i == SLIP_ESC:
            tempSLIPBuffer.append(SLIP_ESC)
            tempSLIPBuffer.append(SLIP_ESC_ESC)
        else:
            tempSLIPBuffer.append(i)
    tempSLIPBuffer.append(SLIP_END)
    return tempSLIPBuffer

# This function uses getSerialByte() function to get SLIP encoded bytes from the serial port and return a decoded byte list  
def decodeFromSLIP(serialFD):
    dataBuffer = []
    while 1:
        serialByte = getSerialByte(serialFD)
        if serialByte is None:
            return -1
        elif serialByte == SLIP_END:
            if len(dataBuffer) > 0:
                return dataBuffer
        elif serialByte == SLIP_ESC:
            serialByte = getSerialByte(serialFD)
            if serialByte is None:
                return -1 
            elif serialByte == SLIP_ESC_END:
                dataBuffer.append(SLIP_END)
            elif serialByte == SLIP_ESC_ESC:
                dataBuffer.append(SLIP_ESC)
            elif serialByte == DEBUG_MAKER:
                dataBuffer.append(DEBUG_MAKER)
            else:
                print("Protocol Error")
        else:
             dataBuffer.append(serialByte)
    return

# This function read byte chuncks from the serial port and return one byte at a time  
def getSerialByte(serialFD):
    if len(readBufferQueue) == 0:
        #fetch a new data chunk from the serial port       
        i = 0
        while len(readBufferQueue) < MAX_MTU:
            newByte = ord(serialFD.read())
            readBufferQueue.append(newByte)
        newByte = readBufferQueue.popleft()
        return newByte
    else:
        newByte = readBufferQueue.popleft()
        return newByte
