#!/usr/bin/python
import curses, curses.panel
from time import sleep
class panelGen:
	def __init__(self, data, stdscr=stdscr):
		self.name = data
		self.stdscr = stdscr
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
		self.fullinfo = self.name, self.window, self.panel, self.rows, self.columns, self.text
		
	def panel(self):
		return self.panel
		#return self.columns, self.rows, self.name
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

def bam(stdscr):
	a = panelGen('hello',stdscr)
	b = panelGen('goodbye',stdscr)
	a.window.addstr(0,0,"FUCK YA")
	a.show()
	curses.panel.update_panels()
	stdscr.refresh()
	sleep(.5)
	b.window.addstr(4,4,"goobyBE")
	b.show()
	b.update()
	stdscr.refresh()
	sleep(.5)


curses.wrapper(bam)
