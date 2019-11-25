#!/usr/bin/python
import curses, curses.panel
import socket, OSC, sliplib, threading, subprocess
from time import sleep

localhost = "127.0.0.1"
sendPD    =  4001
receivePD = localhost, 4000
receiveSer =localhost, 3998
sendSer   =  3999

class panelGen:
	def __init__(self, name, stdscr, columns=41, rows=14, \
				bgcolor=0, subpanels=0, \
				font='/root/tmp/defaultfont.psfu'):
		self.name = name
		self.stdscr = stdscr
		self.columns = columns
		self.rows = rows
		self.bgcolor = bgcolor
		self.subpanels = subpanels
		self.text = 1
		self.pixels=0
		self.font=font #/usr/share/consolefonts/LatArCyrHeb-19.psfu.gz -16 
		self.colors = ['white','black','red','green','yellow','blue','purple','cyan']
		self.window = curses.newwin(self.rows, self.columns,0,0)
		self.window.erase()
		self.panel = curses.panel.new_panel(self.window)
		self.fullinfo = self.name, self.window, self.panel, self.rows, self.columns, self.text
		command = "setfont " + self.font + "<> /dev/tty4 >&0 2>&1"
		subprocess.call(command, shell=True)
		subprocess.call("chvt 4", shell=True) #assumes fbtft_ili9341 connected
	def panel(self):
		return self.panel
	def window(self):
		return self.window
	def show(self):
		self.panel.top()
	def update(self):
		curses.panel.update_panels()
		self.stdscr.refresh()
	def erase(self):
		self.window.erase()
	def _private(self):
		print "iam a nice private func"
	def name(self):
		return self.name 
	def info(self):
		return self.fullinfo
	def columns(self):
		return self.columns
	def rows(self):
		return self.rows
	def string( self, string, y, x, color='white' ):
		if color not in self.colors:
			c = 0
		else:
			c = self.colors.index(color)		
		self.window.addstr( y, x, str(string), curses.A_BOLD | curses.color_pair(c) )	
	def delete( self, length, y, x ) :
		blankline = ""
		for b in xrange(length):
			blankline += " "
		self.window.addstr( y, x, blankline )


stdscr = curses.initscr()
aux = panelGen('aux', stdscr) #needs to be called after wrapper(stdscr)
oled = panelGen('oled', stdscr)
# oscsend 127.0.0.1 3998 /oled/line/1 s "HELLO WORLDS"
# oscsend 127.0.0.1 3998 /oled/line/2 s "HELLO WORLDS2"
# oscsend 127.0.0.1 3998 /oled/line/3 s "HELLO WORLDS3"
# oscsend 127.0.0.1 3998 /oled/line/4 s "HELLO WORLDS4"
# oscsend 127.0.0.1 3998 /oled/line/5 s "HELLO WORLDS5"

def screenLine(addr, tags, data, source): #/oled/line/1-5 and some string shit
	line = int(addr.split("/")[-1])  #last number in OSC address
	temp=''
	for piece in data:
		temp+=str(piece)+' '
	oled.delete( aux.columns, line, 0)
	oled.string( temp, line, 0)
	oled.update()
	oled.show()

def auxLine(addr, tags, data, source):
	line = int(addr.split("/")[-1])  #last number in OSC address
	temp=''
	for piece in data:
		temp+=str(piece)+' '
	aux.delete( oled.columns, line, 0)
	aux.string( temp, line, 0)
	aux.update()
	aux.show()

def shutdown(addr, tags, data, source):
	curses.endwin()
	quit()

def erase(addr, tags, data, source):
	oled.erase()
	oled.update()

def vuMeter(addr, tags, data, source): # /oled/vumeter iiii ADCL ADCR OUTL OUTR
	both = '.'
	left = ':'
	right= ';'
	i=''
	IL=data[0] #MAX  is 19, lowest is 0
	IR=data[1]
	if IR>IL:
		larger=right
	elif IL>IR:
		larger=left
	else:
		larger=both
	for x in xrange(min(IL,IR)):
		i += both
	for x in range(min(IL,IR),max(IL,IR)):
		i += larger
	o=''
	OL=data[2]
	OR=data[3]
	if OR>OL:
		larger=right
	else:
		larger=left
        for x in xrange(min(OL,OR)):
                o += both
        for x in range(min(OL,OR),max(OL,OR)):
                o += larger
	oled.delete(aux.columns, 0,0)
	oled.string("I",0,0)
	oled.string("O",0,aux.columns/2)
	oled.string(i,0,1)
	oled.string(o,0,(aux.columns/2)+1)
	oled.update()
	oled.show()

def initClientComport(ip, port):
	'''needs to be a separate global'''
	global comport
	comport = OSC.OSCClient()
	comport.connect( (ip,port) )

def initClientPD(ip, port):
	global pd
	pd = OSC.OSCClient()
	pd.connect( (ip,port) )

initClientComport ( localhost, sendSer )
initClientPD( localhost, sendPD ) 

def sendOSCComport( address='/print', data=[] ):
	m = OSC.OSCMessage()
	m.setAddress(address)
	for d in data:
		m.append(d)
	comport.send(m)

def sendOSCPD( address='/print', data=[] ):
	m = OSC.OSCMessage()
	m.setAddress(address)
	for d in data:
		m.append(d)
	pd.send(m)



def led(addr, tags, data, source):
	#changes LED state from PD program
	sendOSCComport("/led",data)

def keys(addr, tags, data, source):
	#send keys from STM32 to PD
	sendOSCPD("/key", data)

def knobs(addr, tags, data, source):
	#send knobs from STM32 to PD
	sendOSCPD("/knobs", data)

def quitpd(addr, tags, data, source):
	sendOSCPD("/quitpd",1)


def enc(addr, tags, data, source):
	return 0
def encbutton(addr, tags, data, source):
	return 0

#serial can be sent: /hello, /enablemux, disablemux, /getknobs,  /led

#pd server needs to listen to: /oled/line/X, /oled, /led
#pd needs to be sent: /key, /knobs, /quitpd, 

#server stuff below
serialListener = OSC.ThreadingOSCServer( receiveSer )
pdListener  = OSC.ThreadingOSCServer( receivePD )

#serial listener needs to listen to: /key, /knobs, /enc, /encbut, /hello
serialListener.addMsgHandler("/key", keys) #forward key messages to pd
serialListener.addMsgHandler("/knobs", knobs) #forward knob messages to pd
###############################################################################
serialListener.addMsgHandler("/enc", enc)
serialListener.addMsgHandler("/encbut", encbutton) 
###############################################################################


pdListener.addMsgHandler("/led", led) # handles LED pd -> stm32
for x in range(1,15):
	pdListener.addMsgHandler("/oled/line/"+str(x), screenLine)
pdListener.addMsgHandler("/oled/vumeter", vuMeter) #draws vu meter on line 0
pdListener.addMsgHandler("/erase", erase) #clears screen


SOSC = threading.Thread( target = serialListener.serve_forever )
POSC = threading.Thread( target = pdListener.serve_forever )

SOSC.daemon = True
POSC.daemon = True
SOSC.start()
POSC.start() #send em '
#server stuff above


curses.curs_set(0) #removes blinking cursor
curses.noecho()
curses.start_color()
curses.use_default_colors()
for i in range(0, curses.COLORS):
	curses.init_pair(i+1, i, 0)
stdscr.bkgd(' ', curses.A_BOLD | curses.color_pair(0) ) #black space background


try:
	while True:
		sleep(.1)
except KeyboardInterrupt:

	curses.endwin()
	quit()
#setfont /usr/share/consolefonts/928.cp.gz -16 <> /dev/tty4 >&0 2>&1 #not bad
	#setfont /usr/share/consolefonts/LatGrkCyr-12x22.psfu.gz -16 <> /dev/tty4 >&0 2>&1 HUGE NASTY
	#setfont /usr/share/consolefonts/LatArCyrHeb-19.psfu.gz -16 <> /dev/tty4 >&0 2>&1 not the worst
	#latarcyrheb-sun32.psfu.gz if you are BLIND

