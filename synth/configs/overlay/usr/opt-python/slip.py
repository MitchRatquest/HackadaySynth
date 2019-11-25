#!/usr/bin/env python
import serial
import binascii

# SLIP decoder
class slip():

	def __init__(self):
		self.started = False
		self.escaped = False
		self.stream = ''
		self.packet = ''
		self.SLIP_END = '\xc0'		# dec: 192
		self.SLIP_ESC = '\xdb'		# dec: 219
		self.SLIP_ESC_END = '\xdc'	# dec: 220
		self.SLIP_ESC_ESC = '\xdd'	# dec: 221
		self.serialComm = None

	def append(self, chunk):
		self.stream += chunk.decode('iso-8859-1')

	def decode(self):
		packetlist = []
		for char in self.stream:
			# SLIP_END
			if char == self.SLIP_END:
				if self.started:
					packetlist.append(self.packet)
				else:
					self.started = True
				self.packet = ''
			# SLIP_ESC
			elif char == self.SLIP_ESC:
				self.escaped = True
			# SLIP_ESC_END
			elif char == self.SLIP_ESC_END:
				if self.escaped:
					self.packet += self.SLIP_END
					self.escaped = False
				else:
					self.packet += char
			# SLIP_ESC_ESC
			elif char == self.SLIP_ESC_ESC:
				if self.escaped:
					self.packet += self.SLIP_ESC
					self.escaped = False
				else:
					self.packet += char
			# all others
			else:
				if self.escaped:
					raise Exception('SLIP Protocol Error')
					self.packet = ''
					self.escaped = False
				else:
					self.packet += char
					self.started = True
		self.stream = ''
		self.started = False
		return (packetlist)
		
	def encode(self, packet):
		# Encode an initial END character to flush out any data that 
		# may have accumulated in the receiver due to line noise
		encoded = self.SLIP_END
		for char in packet:
			# SLIP_END
			if char == self.SLIP_END:
				encoded +=  self.SLIP_ESC + self.SLIP_ESC_END
			# SLIP_ESC
			elif char == self.SLIP_ESC:
				encoded += self.SLIP_ESC + self.SLIP_ESC_ESC
			# the rest can simply be appended
			else:
				encoded += char
		encoded += self.SLIP_END
		return (encoded)

