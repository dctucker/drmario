import random

from enums import Flags
from views import Cell as View

class Cell:
	def __init__(self, value=Flags.EMPTY):
		self.value = value

	def __str__(self):
		return View.render(self)

	@classmethod
	def random_color(cls):
		return Flags(Flags.RED * random.randint(1,3))

	def infect(self, color=None):
		if color is None:
			color = self.random_color()
		assert color in (Flags.RED, Flags.YELLOW, Flags.BLUE)
		self.value = Flags(Flags.VIRUS | color)

	def treat(self, color=None, bound=Flags.BIND_NONE):
		if color is None:
			color = self.random_color()
		assert color in (Flags.RED, Flags.YELLOW, Flags.BLUE)
		self.value = Flags(Flags.PILL | color | bound)

	def bind(self, value):
		mask = Flags.BIND_LEFT | Flags.BIND_RIGHT
		self.value &= ~mask
		self.value |= value & mask
		self.value = Flags(self.value)

	def bind_left(self):
		self.bind(Flags.BIND_LEFT)
	def bind_right(self):
		self.bind(Flags.BIND_RIGHT)
	def bind_below(self):
		self.value |= Flags.BIND_BELOW

	def zap(self):
		self.value |= Flags.ZAP
	def unbind(self):
		self.value &= ~(Flags.BIND_LEFT | Flags.BIND_RIGHT | Flags.BIND_BELOW)
	def empty(self):
		self.value = Flags.EMPTY

	def is_empty(self):
		return self.value == Flags.EMPTY
	def color(self):
		return self.value & (Flags.RED | Flags.YELLOW | Flags.BLUE)
	def is_pill(self):
		return self.value & Flags.PILL
	def is_virus(self):
		return self.value & Flags.VIRUS
	def is_zapped(self):
		return self.value & Flags.ZAP == Flags.ZAP
	def is_bound(self):
		return self.value & (Flags.BIND_LEFT | Flags.BIND_RIGHT)
	def is_bound_left(self):
		return self.value & Flags.BIND_LEFT
	def is_bound_right(self):
		return self.value & Flags.BIND_RIGHT
	def is_bound_below(self):
		return self.value & Flags.BIND_BELOW

