#from enum import Enum
import random
import sys

class View:
	def ansi_color(cell):
		return {
			Cell.RED: "\033[37;1;41m",
			Cell.YELLOW: "\033[30;43m",
			Cell.BLUE: "\033[33;1;44m",
			Cell.EMPTY: "\033[0m",
		}[cell.color()]

	def color_str(cell):
		return {
			Cell.RED: "R",
			Cell.YELLOW: "Y",
			Cell.BLUE: "B",
			Cell.EMPTY: ".",
		}[cell.color()]

	def render(cell):
		a = View.ansi_color(cell) 
		c = View.color_str(cell)
		if cell.is_virus():
			c = c.lower()
			c = " %s " % c
		elif cell.is_pill():
			c = c.upper()
			if cell.is_bound_left():
				c = " %s)" % c
			elif cell.is_bound_right():
				c = "(%s " % c
			else:
				c = "(%s)" % c
		else:
			c = " %s " % c
		return "%s%s" % (a, c)

class Cell:
	EMPTY = 0
	PILL = 1
	VIRUS = 2
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

	def empty(self):
		self.value = Cell.EMPTY

	def is_empty(self):
		return self.value == self.EMPTY
	def color(self):
		return self.value & (self.RED | self.YELLOW & self.BLUE)
	def is_virus(self):
		return self.value & self.VIRUS
	def is_pill(self):
		return self.value & self.PILL
	def is_bound(self):
		return self.value & (self.BIND_LEFT | self.BIND_RIGHT)
	def is_bound_left(self):
		return self.value & self.BIND_LEFT
	def is_bound_right(self):
		return self.value & self.BIND_RIGHT

class Bottle:
	def __init__(self, other=None, width=8, height=16):
		self.width = width
		self.height = height
		if other is None:
			self.empty()
		else:
			self.cells = other.cells.copy()

	def __str__(self):
		return "\n" + "\n".join("".join(str(c) for c in row) for row in self.cells) + "\033[0m\n"

	def empty(self):
		self.cells = [[Cell() for row in range(0,self.width)] for col in range(0,self.height)]
	
	def infect(self, level):
		for row in self.cells[3:]:
			for cell in row:
				if random.random() < level / 64.0:
					cell.infect()
	
	def drop_pill(self, pill):
		pill.x = int(self.width / 2) - 1
		pill.y = 1
		self.format_pill(pill)
	
	def format_pill(self, pill):
		x1,y1,x2,y2 = pill.coords()
		pcell1 = self.cell_at(x1,y1)
		pcell2 = self.cell_at(x2,y2)
		if x1 < x2:
			pcell1.value = pill.cell1.value | Cell.BIND_RIGHT
			pcell2.value = pill.cell2.value | Cell.BIND_LEFT
		elif x1 > x2:
			pcell1.value = pill.cell1.value | Cell.BIND_LEFT
			pcell2.value = pill.cell2.value | Cell.BIND_RIGHT
		else:
			pcell1.value = pill.cell1.value
			pcell2.value = pill.cell2.value

	def erase_pill(self, pill):
		x1,y1,x2,y2 = pill.coords()
		pcell1 = self.cells[y1][x1]
		pcell2 = self.cells[y2][x2]
		pcell1.empty()
		pcell2.empty()

	def cell_at(self, col, row):
		if row < 0 or row >= self.height:
			return None
		if col < 0 or col >= self.width:
			return None
		return self.cells[row][col]
	
	def can_move_pill(self, pill, dx, dy, rotation=None):
		copy = Pill(pill)
		copy.move(dx, dy)
		if rotation is not None:
			copy.rotate(rotation)
		x1,y1,x2,y2 = copy.coords()
		cell1 = self.cell_at(x1, y1)
		cell2 = self.cell_at(x2, y2)
		return cell1 and cell2 and cell1.is_empty() and cell2.is_empty()

	def apply_gravity(self):
		for y in range(self.height-1, 0, -1):
			for x,cell in enumerate(self.cells[y]):
				if not cell.is_pill():
					continue
				#if not cell.is_bound():
				#	below = self.cell_at(x,y+1)
				#	if below is None:
				#		continue
				#	if below.is_empty():
				#		self.cell_at(x, y+1).value = cell.value
				#		cell.empty()

class Pill:
	LR = 0
	DU = 1
	RL = 2
	UD = 3
	def __init__(self, other=None):
		if other is None:
			self.cell1 = Cell()
			self.cell2 = Cell()
			self.cell1.treat()
			self.cell2.treat()
			self.rotation = self.LR
		else:
			self.x = other.x
			self.y = other.y
			self.cell1 = other.cell1
			self.cell2 = other.cell2
			self.rotation = other.rotation
	
	def rotate(self, back=False):
		if back:
			self.rotation += 3
		else:
			self.rotation += 1
		self.rotation %= 4

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

	def coords(self):
		return self.xy1() + self.xy2()

	def xy1(self):
		if self.rotation == self.LR:
			return self.x, self.y
		elif self.rotation == self.DU:
			return self.x, self.y
		elif self.rotation == self.RL:
			return self.x + 1, self.y
		elif self.rotation == self.UD:
			return self.x, self.y - 1

	def xy2(self):
		if self.rotation == self.LR:
			return self.x + 1, self.y
		elif self.rotation == self.DU:
			return self.x, self.y - 1
		elif self.rotation == self.RL:
			return self.x, self.y
		elif self.rotation == self.UD:
			return self.x, self.y

class Game:
	def __init__(self, level = 10):
		self.bottle = Bottle()
		self.level = level
		self.time = 0
	
	def display(self):
		return str(self.bottle)

	def begin(self):
		self.bottle.empty()
		self.bottle.infect(self.level)

	def toss_pill(self):
		self.pill = Pill()
		self.bottle.drop_pill(self.pill)

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
	
	def tick(self):
		if self.pill is None:
			self.toss_pill()
		self.bottle.apply_gravity()
		self.move_down()

