#!/usr/bin/python
import curses, curses.panel
import socket, OSC, sliplib, threading, time, subprocess
localhost = "127.0.0.1"
sendPD    = 4001
receivePD = 4000
receiveSer =3998
sendSer   = 3999

serReceive = localhost,receiveSer
pdReceive = localhost, receivePD

def initOSCClient(ip, port):
	global client 
	client = OSC.OSCClient()
	client.connect( (ip,port) )

def printing_handler(addr, tags, data, source):
	mesothelioma = str(addr[-1])
	print "---------"
	print "with addr : %s" % addr
	print "addr[-1] : %s" % mesothelioma
	print "typetags :%s" % tags
	print "the actual data is : %s" % data
	print "---"

def sendOSCMsg( address='/print', data=[] ):
	m = OSC.OSCMessage()
	m.setAdress(address)
	for d in data:
		m.append(d)
	client.send(m)

serialOSC = OSC.ThreadingOSCServer( serReceive )
pdOSC  = OSC.ThreadingOSCServer( pdReceive )

initOSCClient( localhost, sendSer )
initOSCClient( localhost, sendPD, )

serialOSC.addMsgHandler("/test", printing_handler)
pdOSC.addMsgHandler("/test", printing_handler)

SOSC = threading.Thread( target = serialOSC.serve_forever )
POSC = threading.Thread( target = pdOSC.serve_forever )

SOSC.daemon = True
POSC.daemon = True
SOSC.start()
POSC.start() #send em '/test'

class panelGen:
	def __init__(self, data):
		self.name = data
		
		#self.height=15
		self.columns=40
		self.rows=15
		self.bgcolor=0
		self.subpanels=0
		self.text=1
		self.pixels=0
		self.font='default'
		
		self.window = curses.newwin(self.rows, self.columns,0,0)
		self.window.erase()
		self.panel = curses.panel.new_panel(self.window)
		self.fullinfo = self.name, self.window, self.panel
		
	def getPanel(self):
		return self.columns, self.rows, self.name
	def getWindow(self):
		return self.window
	def show(self):
		self.panel.top()
	def update(self):
		curses.panel.update_panels()
	def _private(self):
		print "iam a nice private func"
	def getName(self):
		return self.name
	def getInfo(self):
		return self.name, self.window, self.panel

class panelMan:
	def __init__(self,name):
		self.name=name
		self.panels=[]
		
	def addPanel(self,panel):
		self.panels.append(panel.getInfo) #name, window, panel
	def showPanel(self, panel):
		if panel.getName in self.panels:
			self.panels[panel.getName]
		

def cursesLoop(stdscr):
#	command = "setsid sh -c 'exec python /root/python/threadingserver.py <> /dev/tty4 >&0 2>&1'"
	command = "chvt 4"
	subprocess.call(command,shell=True)
	try:
		curses.curs_set(0)
	except:
		pass
	curses.start_color()
	curses.use_default_colors()
	for i in range(0, curses.COLORS):
		curses.init_pair(i+1, i, 0)
	stdscr.bkgd(' ', curses.A_BOLD | curses.color_pair(0))
	stdscr.addstr(0,0,"hello, world!")	
	curses.panel.update_panels()
	stdscr.refresh()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt :
		#s.close()
		#st.join()
		quit()

def begin_curses():
	curses.wrapper(cursesLoop)

begin_curses()
