import random

class Cell:
	EMPTY = 0
	PILL = 1
	VIRUS = 2
	ZAP = 3
	RED = 4
	YELLOW = 8
	BLUE = 12
	BIND_NONE = 0
	BIND_LEFT = 16
	BIND_RIGHT = 32

	def __init__(self, value=EMPTY):
		self.value = value

	def __str__(self):
		return View.render(self)

	@classmethod
	def random_color(cls):
		return cls.RED * random.randint(1,3)

	def infect(self, color=None):
		if color is None:
			color = self.random_color()
		assert color in (self.RED, self.YELLOW, self.BLUE)
		self.value = self.VIRUS | color

	def treat(self, color=None, bound=BIND_NONE):
		if color is None:
			color = self.random_color()
		assert color in (self.RED, self.YELLOW, self.BLUE)
		self.value = self.PILL | color | bound

	def bind(self, value):
		mask = self.BIND_LEFT | self.BIND_RIGHT
		self.value &= ~mask
		self.value |= value & mask

	def bind_left(self):
		self.bind(self.BIND_LEFT)
	def bind_right(self):
		self.bind(self.BIND_RIGHT)

	def zap(self):
		self.value |= Cell.ZAP
	def unbind(self):
		self.value &= ~ (Cell.BIND_LEFT | Cell.BIND_RIGHT)
	def empty(self):
		self.value = Cell.EMPTY

	def is_empty(self):
		return self.value == self.EMPTY
	def color(self):
		return self.value & (self.RED | self.YELLOW & self.BLUE)
	def is_pill(self):
		return self.value & self.PILL
	def is_virus(self):
		return self.value & self.VIRUS
	def is_zapped(self):
		return self.value & self.ZAP == self.ZAP
	def is_bound(self):
		return self.value & (self.BIND_LEFT | self.BIND_RIGHT)
	def is_bound_left(self):
		return self.value & self.BIND_LEFT
	def is_bound_right(self):
		return self.value & self.BIND_RIGHT

class View:
	def ansi_color(cell):
		return {
			Cell.RED: "\033[0;30;41;4m",
			Cell.YELLOW: "\033[0;30;43;4m",
			Cell.BLUE: "\033[0;30;46;4m",
			Cell.EMPTY: "\033[0;34;40m",
		}[cell.color()]

	def color_str(cell):
		return {
			Cell.RED: "▌Ѧ▐",
			Cell.YELLOW: "▌Ѡ▐",
			Cell.BLUE: "▌Ж▐",
			Cell.EMPTY: " - ",
		}[cell.color()]

	def render(cell):
		a = View.ansi_color(cell) 
		c = View.color_str(cell)
		if cell.is_zapped():
			c = "\033[24;7m>@<\033[27m"
		elif cell.is_pill():
			c = " "
			if cell.is_bound_left():
				c = "│%s▐" % c
			elif cell.is_bound_right():
				c = "▌%s│" % c
			else:
				c = "▌%s▐" % c
		return "%s%s" % (a, c)

