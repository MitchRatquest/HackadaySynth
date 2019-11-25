#!/usr/bin/python
import curses, curses.panel
from time import sleep
import subprocess
class panelGen:
	def __init__(self, name, stdscr, columns=15, rows=40, \
				bgcolor=0, subpanels=0, font='default'):
		self.name = name
		self.stdscr = stdscr
		self.columns = columns
		self.rows = rows
		self.bgcolor = bgcolor
		self.subpanels = subpanels
		self.text = 1
		self.pixels=0
		self.font='default'
		self.colors = ['white','black','red','green','yellow','blue','purple','cyan']
		self.window = curses.newwin(self.rows, self.columns,0,0)
		self.window.erase()
		self.panel = curses.panel.new_panel(self.window)
		self.fullinfo = self.name, self.window, self.panel, self.rows, self.columns, self.text
		
	def panel(self):
		return self.panel
	def window(self):
		return self.window
	def show(self):
		self.panel.top()
	def update(self):
		curses.panel.update_panels()
		self.stdscr.refresh()
	def _private(self):
		print "iam a nice private func"
	def name(self):
		return self.name
	def info(self):
		return self.fullinfo
	def string(self, string, y, x, color='white'):
		if color not in self.colors:
			c = 0
		else:
			c = self.colors.index(color)		
		self.window.addstr( y, x, str(string), curses.A_BOLD | curses.color_pair(c))	
	def fuck ( self, length, y, x ) :
		blankline = ""
		for b in xrange(length):
			blankline += " "		
		self.window.addstr( y, x, blankline)



def bam(stdscr):
	command = "setsid sh -c 'setfont /usr/share/consolefonts/Mik_8x16.gz <> /dev/tty4 >&0 2>&1'"
        subprocess.call(command, shell=True)
	curses.curs_set(0)
	curses.start_color()
	curses.use_default_colors()
	for i in range(0, curses.COLORS):
		curses.init_pair(i+1, i, 0)
	stdscr.bkgd(' ', curses.A_BOLD | curses.color_pair(0 ) )

	a = panelGen('hello',stdscr,columns=60)
	b = panelGen('goodbye',stdscr)
#	for x in xrange(10):
#		a.string("FUCKYAAAAAAAAAAAAAAAAAAA", x,0)
	a.string("oh YAAAA",0,0,'cyan')
#	a.window.addstr(0,0,"FUCK YA")
	a.show()
	a.update()
	sleep(.5)
	a.fuck(11,0,0)
#	a.string("            ",0,0)
	a.show()
	a.update()
	sleep(.5)
	b.window.addstr(4,4,"goobyBE")
	b.show()
	b.update()
	sleep(.5)
	chamble = [a,b]
	for x in chamble:
#		command = "echo " + x.name + " > /dev/tty8" 
#		subprocess.call(command,shell=True)
		b.string(x.name,0,0)
		b.update()
		sleep(.5)
curses.wrapper(bam)
