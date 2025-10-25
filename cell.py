"""provides the Cell class"""

import random

from enums import Flags
from views import Cell as View

class Cell:
	"""models a cell within the bottle"""

	def __init__(self, value=Flags.EMPTY):
		self.value = value

	def __str__(self):
		return View.render(self)

	@classmethod
	def random_color(cls):
		"""returns a Flag representing a randomly selected color"""
		return Flags(Flags.RED * random.randint(1,3))

	def infect(self, color=None):
		"""set this cell to a virus of random color"""
		if color is None:
			color = self.random_color()
		assert color in (Flags.RED, Flags.YELLOW, Flags.BLUE)
		self.value = Flags(Flags.VIRUS | color)

	def treat(self, color=None, bound=Flags.BIND_NONE):
		"""set this cell to have a pill of a given color and binding"""
		if color is None:
			color = self.random_color()
		assert color in (Flags.RED, Flags.YELLOW, Flags.BLUE)
		self.value = Flags(Flags.PILL | color | bound)

	def bind(self, value):
		"""apply the given binding flags to this cell"""
		mask = Flags.BIND_LEFT | Flags.BIND_RIGHT
		self.value &= ~mask
		self.value |= value & mask
		self.value = Flags(self.value)

	def bind_left(self):
		"""bind this cell on the left"""
		self.bind(Flags.BIND_LEFT)

	def bind_right(self):
		"""bind this cell on the right"""
		self.bind(Flags.BIND_RIGHT)

	def bind_below(self):
		"""bind this cell below"""
		self.value |= Flags.BIND_BELOW

	def zap(self):
		"""zap this cell"""
		self.value |= Flags.ZAP

	def unbind(self):
		"""clear the bindings of this cell"""
		self.value &= ~(Flags.BIND_LEFT | Flags.BIND_RIGHT | Flags.BIND_BELOW)

	def empty(self):
		"""set this cell to empty value"""
		self.value = Flags.EMPTY

	def is_empty(self):
		"""return True if this cell is empty"""
		return self.value == Flags.EMPTY

	def color(self):
		"""return True if this cell contains a pill or virus of any color"""
		return self.value & (Flags.RED | Flags.YELLOW | Flags.BLUE)

	def is_pill(self):
		"""return True if this cell contains a pill"""
		return self.value & Flags.PILL

	def is_virus(self):
		"""return True if this cell contains a virus"""
		return self.value & Flags.VIRUS

	def is_zapped(self):
		"""return True if this cell has been zapped"""
		return self.value & Flags.ZAP == Flags.ZAP

	def is_bound(self):
		"""return True if this cell has bindings"""
		return self.value & (Flags.BIND_LEFT | Flags.BIND_RIGHT)

	def is_bound_left(self):
		"""return True if this cell is bound to the left"""
		return self.value & Flags.BIND_LEFT

	def is_bound_right(self):
		"""return True if this cell is bound to the right"""
		return self.value & Flags.BIND_RIGHT

	def is_bound_below(self):
		"""return True if this cell is bound below"""
		return self.value & Flags.BIND_BELOW

