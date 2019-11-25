import ProtoSLIP
import termios
import serial

# This function connect and configure the serial port. Then returns the file discripter  
def connectToSerialPort():
    port = '/dev/ttyS0'
    serialFD = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, xonxoff=False, rtscts=False)
    # port='/dev/ttyUSB0'- port to open  
    # baudrate=115200  - baud rate to communicate with the port  
    # bytesize=8           - size of a byte  
    # parity='N'           - no parity  
    # stopbits=1           - 1 stop bit  
    # xonxoff=False           - no software handshakes  
    # rtscts=False           - no hardware handshakes  
    if serialFD < 0:
        print("Couldn't open serial port")
        return -1
    else:
        print("Opened serial port")
        return serialFD

# This function accept a byte array and write it to the serial port  
def writeToSerialPort(serialFD, byteArray):
    encodedSLIPBytes = ProtoSLIP.encodeToSLIP(byteArray)
    #convert byte list to a string
    byteString = ''.join(chr(b) for b in encodedSLIPBytes)
    serialFD.write(byteString)
    return


# This function reads from the serial port and return a byte array  
def readFromSerialPort(serialFD):
    i = 1
    byteArray = None
    byteArray = ProtoSLIP.decodeFromSLIP(serialFD)
    if byteArray is None:
        print "readFromSerialPort(serialFD): Error"
        return -1
    else:
        return byteArray

# This function reads from the serial port and return a byte array  
def disconnectFromSerialPort(serialFD):
    serialFD.close()
    return

if __name__ == '__main__':
    ser = connectToSerialPort()
    ya= readFromSerialPort(ser)
    string=''
    for x in ya:
        string+=chr(x)
    print string
    writeToSerialPort(ser,[48,49,51,52,53,54,55,56,57])
