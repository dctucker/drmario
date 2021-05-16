import os, sys
try:
   import colorama
   colorama.init()
except:
   try:
       import tendo.ansiterm
   except:
       pass

import atexit

def is_nt():
	return os.name == 'nt'

if not is_nt():
	import termios, fcntl

class Term:
	def __init__(self):
		if is_nt():
			self.init_nt()
		else:
			self.init_posix()

	def init_posix(self):
		os.system('clear')
		self.fd = sys.stdin.fileno()

		self.oldterm = termios.tcgetattr(self.fd)
		self.newattr = termios.tcgetattr(self.fd)
		self.newattr[3] = self.newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(self.fd, termios.TCSANOW, self.newattr)

		self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

		atexit.register(self.cleanup_posix)

	def cleanup_posix(self):
		termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

	def init_nt(self):
		os.system('cls')
		# msvcrt
		pass
	
	def getch(self):
		if is_nt():
			pass
		else:
			ret = ""
			c = " "
			while c != "":
				c = sys.stdin.read(1)
				ret += c
			return ret

	def clear(self):
		if is_nt():
			os.system('cls')
		else:
			print('\033[J\033[H')
			#os.system('clear')


