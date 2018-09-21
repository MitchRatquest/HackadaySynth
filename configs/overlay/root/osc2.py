#!/usr/bin/python
import socket, OSC, threading, time, re, subprocess
from time import sleep
import curses, curses.panel

flag =0 

receive_address = '127.0.0.1',9999
send_address    = receive_address[0]
send_port       = 9998

def initOSCClient(ip, port) :
    global client
    client = OSC.OSCClient()
    client.connect( (ip,port) )
    
def printing_handler(addr, tags, data, source):
    print "---"
    print "with addr : %s" % addr
    print "typetags :%s" % tags
    print "the actual data is : %s" % data
    print "---"
    
def sendOSCMsg( address='/print', data=[] ) :
    m = OSC.OSCMessage()
    m.setAddress(address)
    for d in data :
        m.append(d)
    client.send(m)

s = OSC.ThreadingOSCServer(receive_address)
initOSCClient(send_address, send_port)
s.addMsgHandler("/test", printing_handler) # adding our function, first parameter corresponds to the OSC address you want to listen to
#-------------------------------------
def echo_handler(addr, tags, data, source):
	sendOSCMsg("/echo",data)

s.addMsgHandler("/echo", echo_handler)
#-------------------------------------
def display_handler(addr, tags, data, source):
	print "got %s" % data
	print "i received this many items: %d" % len(data)
	for i in range(0,len(data)):
		print data[i]
s.addMsgHandler("/displayelement", display_handler)
#--------shit gets weird below here

def addstring(addr, tags, data, source):
	#string, y, x, color, panel
	index = -1
	for x in range(0,len(panelNames)):
		if data[4] == panelNames[x][0]:
			index = x
			break
	if index == -1: #there is no panel named data[4]
		return
	currentwindow = panelNames[index][1] #should be window
	currentpanel = panelNames[index][2]
	data[0] = str(data[0]).replace("_"," ")	#turn underscores to spaces

	color = 0
	for x in range(0,8):
		if data[3] == colors[x]:
			color=x
			break		
	try:
		currentwindow.addstr(data[1],data[2],str(data[0]),curses.A_BOLD | curses.color_pair(color))
	except:
		pass
	flag = 1
	curses.panel.update_panels()
	
s.addMsgHandler("/addstring", addstring)

panelNames=[] #nested array of [name, window, panel],[name, window, panel]

def addpanel(addr, tags, data, source):
	#panel, create panel
	index = -1
	for x in range(0,len(panelNames)):
		if data[0] == panelNames[x][0]:
			index = x
			break
	if index >= 0: #there is already a panel with this name
		return
	newwindow = curses.newwin(HEIGHT, WIDTH,0,0)
	newwindow.erase()
	newpanel = curses.panel.new_panel(newwindow)
	panelArray=[data[0], newwindow, newpanel]
	panelNames.append(panelArray)
	newpanel.top()
	curses.panel.update_panels()
	
s.addMsgHandler("/addpanel", addpanel)

def deletestring(addr, tags, data, source):
	#length, x, y, panel
	length = data[0]
	index = 0
	try:
		for k in range(0,len(panelNames)):
			if data[3] == panelNames[k][0]:
				index = k
				break
	except:
		return

	currentwindow = panelNames[index][1] #should be window
	blankstring=''
	for x in range(0,length):
		blankstring += ' '
	try:
		currentwindow.addstr(data[1],data[2],str(blankstring)) #works way better than delch
	except:
		pass
	curses.panel.update_panels()
	flag =1 
s.addMsgHandler("/deletestring", deletestring)

def focuspanel(addr, tags, data, source):
	#panel
	for k in range(0,len(panelNames)):
		if data[0] == panelNames[k][0]:
			index = k
			break
	panelNames[index][2].top()
s.addMsgHandler("/focuspanel", focuspanel)

########GOOFY SHIT WRT NCURSES
def pixelterminal(addr, tags, data, source):
	if(data[0]) == 1: #you turn that tty into a piece of crap
		command = "setsid sh -c 'setfont /usr/share/consolefonts/1pix-1x1.psfu  <> /dev/tty3 >&0 2>&1'"
		subprocess.call(command, shell=True)
		COLUMNS=320
		WIDTH=320
		ROWS=240
		HEIGHT=240
	if(data[0]) == 0: #save that tty from hell
		command = "setsid sh -c 'setfont /usr/share/consolefonts/Mik_8x16.gz <> /dev/tty3 >&0 2>&1'"
		subprocess.call(command, shell=True)
		COLUMNS=40
		WIDTH=40
		ROWS=15
		HEIGHT=15

s.addMsgHandler("/pixelterminal", pixelterminal)

COLUMNS=40
WIDTH=40
ROWS=15
HEIGHT=15

side = 60    # <
top  = 126   # ~
bottom = 95  # _

colors=['white','black','red','green','yellow','blue','purple','cyan']
#######
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr
################
st = threading.Thread( target = s.serve_forever )
st.start()
'''
curses.initscr()
try:
	while True:
		sendOSCMsg('/hello',[int(b)])
		time.sleep(1)
		b+=1
except KeyboardInterrupt :
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
'''

#CURSES
def make_panel(h,l, y,x, str):
	win = curses.newwin(h,l, y,x)
	win.erase()
	win.border(side, side,  top, bottom,    side,    side,     side,     side)
	# win.box(curses.ACS_RARROW,curses.ACS_BULLET)
	win.addstr(2, 2, str)

	panel = curses.panel.new_panel(win)
	return win, panel

def test(stdscr):
	command = "setsid sh -c 'setfont /usr/share/consolefonts/Mik_8x16.gz <> /dev/tty1 >&0 2>&1'"
        subprocess.call(command, shell=True)

	try:
		curses.curs_set(0)
	except:
		pass
	curses.start_color()
	curses.use_default_colors() 
	for i in range(0, curses.COLORS):
		curses.init_pair(i+1, i, 0)
	string = "panels forever"
	stdscr.bkgd(' ', curses.A_BOLD | curses.color_pair(0 ) )
	stdscr.addstr(0, 10, str(curses.color_pair(1)))
	for x in range(0, 8):
		stdscr.addstr(x, (COLUMNS/2-(len(string)/2)), string,curses.color_pair(x)) 
		stdscr.addstr(9, (COLUMNS/2-(len(str(curses.COLORS)))), str(curses.COLORS) )
		stdscr.addstr(12, 0, str(curses.color_pair(4)),curses.color_pair(1)|curses.color_pair(2))
	stdscr.hline(10,0,'-',40) 
	#
	command = "setsid sh -c 'chvt 3'"
	subprocess.call(command,shell=True)
	#
	curses.panel.update_panels()
	stdscr.refresh()
	sleep(1)
	curses.panel.update_panels()
	stdscr.refresh()
	sleep(1)
	flag = 0
	try:
		while True:
			if flag==0:
				curses.panel.update_panels()
				stdscr.refresh()
				flag = 0
			sleep(.1)
	except KeyboardInterrupt :
		print "\nClosing OSCServer."
		s.close()
		print "Waiting for Server-thread to finish"
		st.join() ##!!!
		print "Done"
		quit()

if __name__ == '__main__':
	global test
	curses.wrapper(test)

