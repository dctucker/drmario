"""provides terminal functionality for POSIX and Windows NT"""

import os
import sys
import atexit

def is_nt():
	"""return True when running on Windows NT"""
	return os.name == 'nt'

#pylint: disable=bare-except,import-error,possibly-used-before-assignment,unused-import
try:
	import colorama
	colorama.init()
except:
	try:
		import tendo.ansiterm
	except:
		pass

if is_nt():
	import msvcrt
else:
	import termios
	import fcntl

class Term:
	"""models the terminal"""

	KEY_LEFT  = ('\033[D', '\xe0K')
	KEY_RIGHT = ('\033[C', '\xe0M')
	KEY_DOWN  = ('\033[B', '\xe0P')

	def __init__(self):
		if is_nt():
			self.init_nt()
		else:
			self.init_posix()

	def init_posix(self):
		"""initialize POSIX terminal by clearning and setting the appropriate file descriptor flags"""
		os.system('clear')
		self.fd = sys.stdin.fileno()

		self.oldterm = termios.tcgetattr(self.fd)
		self.newattr = termios.tcgetattr(self.fd)
		self.newattr[3] = self.newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(self.fd, termios.TCSANOW, self.newattr)

		self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

		atexit.register(self.cleanup_posix)

	def block(self):
		"""set flags to block the terminal"""
		if is_nt():
			return
		termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

	def unblock(self):
		"""unset flags blocking the terminal"""
		if is_nt():
			return
		termios.tcsetattr(self.fd, termios.TCSANOW, self.newattr)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

	def cleanup_posix(self):
		"""return the terminal to a state suitable for the POSIX command line"""
		self.block()
		print("\033[?25h")

	def init_nt(self):
		"""initialize Windows NT terminal"""
		os.system('cls')
		atexit.register(self.cleanup_nt)

	def cleanup_nt(self):
		"""return the terminal to a state suitable for the NT command line"""
		print("\033[?25h")

	def getch(self):
		"""get a character from STDIN"""
		ret = ""
		c = " "
		if is_nt():
			while c != "":
				if msvcrt.kbhit():
					c = msvcrt.getch()
					ret += ''.join(chr(x) for x in c)
				else:
					c = ""
		else:
			while c != "":
				c = sys.stdin.read(1)
				ret += c
		return ret

	def display(self, s):
		"""blocking method to print control characters to the terminal"""
		self.block()
		self.clear()
		print(str(s))
		self.unblock()

	def clear(self):
		"""clear the terminal"""
		print('\033[?25l\033[J\033[H')

