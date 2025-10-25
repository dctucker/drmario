"""provides the class for the game"""

import time

from enums import State, Speed
from bottle import Bottle
from pill import Pill
from views import Game as View

class Game:
	"""models the game and all its moving pieces"""
	#pylint: disable=too-many-instance-attributes

	def __init__(self, level = 1, speed = Speed.MED):
		self.level = level
		self.speed = Speed(speed)
		self.bottle = None
		self.next_pill = None
		self.pill = None
		self.state = State.PAUSED
		self.previous_state = State.QUIT
		self.ticked = 0
		self.zapped = 0
		self.combo = 0
		self.score = 0
		self.delay = 0
		self.setup()

	def setup(self):
		"""set the initial values for the game"""
		self.bottle = Bottle()
		self.next_pill = Pill()
		self.reset_delay()
		self.state = State.MOVING
		self.ticked = 0
		self.zapped = 0
		self.combo = 0
		self.score = 0

	def __str__(self):
		return View.render(self)

	def begin(self):
		"""empty the bottle and add viruses based on the chosen difficulty"""
		self.bottle.empty()
		self.bottle.infect(self.level * 4)

	def toss_pill(self):
		"""toss the next pill into the bottle and return the pill"""
		self.pill = self.next_pill
		toss = self.bottle.toss_pill(self.pill)
		self.next_pill = Pill()
		return toss

	def rotate_pill(self, back = False):
		"""rotate the pill by 90 degrees clockwise or counter-clockwise"""
		if self.pill is None:
			return
		self.bottle.erase_pill(self.pill)
		if self.bottle.can_move_pill(self.pill, 0, 0, back):
			self.pill.rotate(back)
		else:
			if self.bottle.can_move_pill(self.pill, -1, 0, back):
				self.pill.move(-1, 0)
				self.pill.rotate(back)
		self.bottle.format_pill(self.pill)

	def rotate_pill_back(self):
		"""rotate the pill counter-clockwise"""
		self.rotate_pill(back=True)

	def move_left(self):
		"""move the pill left if possible"""
		if self.pill is None:
			return
		self.bottle.erase_pill(self.pill)
		if self.bottle.can_move_pill(self.pill, -1, 0):
			self.pill.move(-1, 0)
		self.bottle.format_pill(self.pill)

	def move_right(self):
		"""move the pill right if possible"""
		if self.pill is None:
			return
		self.bottle.erase_pill(self.pill)
		if self.bottle.can_move_pill(self.pill, 1, 0):
			self.pill.move(1, 0)
		self.bottle.format_pill(self.pill)

	def move_down(self):
		"""move the pill down"""
		if self.pill is None:
			return
		self.bottle.erase_pill(self.pill)
		if self.bottle.can_move_pill(self.pill, 0, 1):
			self.pill.move(0, 1)
			self.bottle.format_pill(self.pill)
		else:
			self.bottle.format_pill(self.pill)
			self.pill = None

	def slam_pill(self):
		"""move the pill all the way down"""
		if self.pill is None:
			return
		self.bottle.erase_pill(self.pill)
		dy = 0
		while self.bottle.can_move_pill(self.pill, 0, dy+1):
			dy += 1
		self.pill.move(0, dy)
		self.bottle.format_pill(self.pill)
		self.pill = None

	def reset_delay(self):
		"""reset the game speed to the chosen value"""
		bpms = ( 85.5, 185.3, 235.0 )
		self.delay = 60.0 / bpms[self.speed]

	def tick(self):
		"""perform one iteration of game movement"""
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
				self.score += 100 * (self.speed + 1) * 2 ** (zapped - 1)
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
		"""check for aligned pill that can be zapped"""
		return self.bottle.zap_aligned()

	def toggle_pause(self):
		"""pause or unpause the game"""
		if self.state == State.PAUSED:
			self.unpause()
		else:
			self.pause()

	def pause(self):
		"""pause the game"""
		self.previous_state = self.state
		self.state = State.PAUSED

	def unpause(self):
		"""unpause the game"""
		self.state = State(self.previous_state)
		del self.previous_state

	def restart(self):
		"""restart the game"""
		self.setup()
		self.begin()
		self.toss_pill()

	def is_paused(self):
		"""return True if the game is paused"""
		return self.state == State.PAUSED

	def win(self):
		"""return True if the game has been won"""
		return self.state == State.WIN

	def lose(self):
		"""return True if the game has been lost"""
		return self.state == State.LOSE

	def over(self):
		"""return True if the game is no longer active"""
		return self.state in (State.WIN, State.LOSE)

	def has_quit(self):
		"""return True if the user wants to quit the game"""
		return self.state == State.QUIT

	def quit(self):
		"""quit the game"""
		self.state = State.QUIT

