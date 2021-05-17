from cell import Cell
from views import Pill as View

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
			self.cell1.bind_right()
			self.cell2.bind_left()
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
	
	def bind_ltr(self):
		self.cell1.bind_left()
		self.cell2.bind_right()
	def bind_rtl(self):
		self.cell1.bind_right()
		self.cell2.bind_left()
	def unbind(self):
		self.cell1.unbind()
		self.cell2.unbind()

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

	def __str__(self):
		return View.render(self)

