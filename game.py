#from enum import Enum
import sys
import time

from bottle import Bottle
from pill import Pill

class State:
	DROPPED = 0
	FALLING = 1
	NEW_PILL = 2
	

class Game:
	def __init__(self, level = 10):
		self.bottle = Bottle()
		self.level = level
		self.delay = 1
		self.speed = 1
		self.ticked = 0
		self.zapped = False
		self.gravity_done = False
		self.state = State.DROPPED
		self.next_pill = Pill()
	
	def display(self):
		next_pill = str(self.next_pill)
		bottle = str(self.bottle)
		stats = ""
		stats += "PILL " if self.pill is not None else "     "
		stats += "STATE: %d" % self.state
		return "%s\n%s\n%s" % (next_pill, bottle, stats)

	def begin(self):
		self.bottle.empty()
		self.bottle.infect(self.level)

	def toss_pill(self):
		self.pill = self.next_pill
		self.bottle.drop_pill(self.pill)
		self.next_pill = Pill()

	def rotate_pill(self, back = False):
		if self.pill is None: return
		self.bottle.erase_pill(self.pill)
		if self.bottle.can_move_pill(self.pill, 0, 0, back):
			self.pill.rotate(back)
		else:
			if self.bottle.can_move_pill(self.pill, -1, 0, back):
				self.pill.move(-1, 0)
				self.pill.rotate(back)
		self.bottle.format_pill(self.pill)

	def move_left(self):
		if self.pill is None: return
		self.bottle.erase_pill(self.pill)
		if self.bottle.can_move_pill(self.pill, -1, 0):
			self.pill.move(-1, 0)
		self.bottle.format_pill(self.pill)

	def move_right(self):
		if self.pill is None: return
		self.bottle.erase_pill(self.pill)
		if self.bottle.can_move_pill(self.pill, 1, 0):
			self.pill.move(1, 0)
		self.bottle.format_pill(self.pill)

	def move_down(self):
		if self.pill is None: return
		self.bottle.erase_pill(self.pill)
		if self.bottle.can_move_pill(self.pill, 0, 1):
			self.pill.move(0, 1)
			self.bottle.format_pill(self.pill)
		else:
			self.bottle.format_pill(self.pill)
			self.pill = None

	def reset_delay(self):
		self.delay = 1.0 / self.speed
	
	def tick(self):
		now = time.time()
		if now - self.ticked < self.delay:
			return False
		self.ticked = now

		if self.pill is not None:
			self.move_down()
		else:
			self.delay = 0.25
			if self.state == State.DROPPED:
				zapped = self.check_aligned()
				if zapped:
					self.state = State.FALLING
				else:
					self.state = State.NEW_PILL
			elif self.state == State.FALLING:
				self.bottle.clear_zapped()
				if self.bottle.apply_gravity() == 0:
					self.state = State.DROPPED
			elif self.state == State.NEW_PILL:
				self.toss_pill()
				self.reset_delay()
				self.state = State.DROPPED
		return True

	def check_aligned(self):
		return self.bottle.zap_aligned()

