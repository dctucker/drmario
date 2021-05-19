import sys
import time

from enums import State
from bottle import Bottle
from pill import Pill
from views import Game as View

class Game:
	def __init__(self, level = 1, speed = 1):
		self.bottle = Bottle()
		self.level = level
		self.speed = speed

		self.reset_delay()
		self.ticked = 0
		self.zapped = False
		self.gravity_done = False
		self.state = State.MOVING
		self.next_pill = Pill()
		self.combo = 0

	def __str__(self):
		return View.render(self)

	def begin(self):
		self.bottle.empty()
		self.bottle.infect(self.level * 4)

	def toss_pill(self):
		self.pill = self.next_pill
		toss = self.bottle.toss_pill(self.pill)
		self.next_pill = Pill()
		return toss

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

	def rotate_pill_back(self):
		self.rotate_pill(back=True)

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

	def slam_pill(self):
		if self.pill is None: return
		self.bottle.erase_pill(self.pill)
		potential = True
		dy = 0
		while self.bottle.can_move_pill(self.pill, 0, dy+1):
			dy += 1
		self.pill.move(0, dy)
		self.bottle.format_pill(self.pill)
		self.pill = None

	def reset_delay(self):
		bpms = [ 85.5, 185.3, 235.0 ]
		self.delay = 60.0 / bpms[self.speed]
	
	def tick(self):
		now = time.time()
		if now - self.ticked < self.delay:
			return False
		self.ticked = now

		if self.state == State.PAUSED:
			return False
		if self.state == State.MOVING:
			if self.pill is not None:
				self.move_down()
			if self.pill is None:
				self.combo = 0
				self.delay = 0.25
				self.state = State.DROPPED
		if self.state == State.DROPPED:
			zapped = self.check_aligned()
			if zapped:
				self.combo += zapped
				if self.bottle.virus_count() == 0:
					self.state = State.WIN
					return True
				self.state = State.FALLING
			else:
				self.state = State.NEW_PILL
		elif self.state == State.FALLING:
			self.bottle.clear_zapped()
			if self.bottle.apply_gravity() == 0:
				self.state = State.DROPPED
		elif self.state == State.NEW_PILL:
			if self.toss_pill():
				self.reset_delay()
				self.state = State.MOVING
			else:
				self.state = State.LOSE
				return False
		return True

	def check_aligned(self):
		return self.bottle.zap_aligned()

	def toggle_pause(self):
		if self.state == State.PAUSED:
			self.unpause()
		else:
			self.pause()

	def pause(self):
		self.previous_state = self.state
		self.state = State.PAUSED

	def unpause(self):
		self.state = self.previous_state
		del self.previous_state

	def is_paused(self):
		return self.state == State.PAUSED

	def win(self):
		return self.state == State.WIN

	def lose(self):
		return self.state == State.LOSE

	def has_quit(self):
		return self.state == State.QUIT

	def quit(self):
		self.state = State.QUIT

