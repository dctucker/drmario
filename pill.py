from enums import Orientation
from cell import Cell
from views import Pill as View

class Pill:
	def __init__(self, other=None):
		if other is None:
			self.cell1 = Cell()
			self.cell2 = Cell()
			self.cell1.treat()
			self.cell2.treat()
			self.cell1.bind_right()
			self.cell2.bind_left()
			self.rotation = Orientation.LR
		else:
			self.x = other.x
			self.y = other.y
			self.cell1 = other.cell1
			self.cell2 = other.cell2
			self.rotation = Orientation(other.rotation)
	
	def rotate(self, back=False):
		rot = self.rotation + (3 if back else 1)
		self.rotation = Orientation(rot % 4)

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
		if self.rotation == Orientation.LR:
			return self.x, self.y
		elif self.rotation == Orientation.DU:
			return self.x, self.y
		elif self.rotation == Orientation.RL:
			return self.x + 1, self.y
		elif self.rotation == Orientation.UD:
			return self.x, self.y - 1

	def xy2(self):
		if self.rotation == Orientation.LR:
			return self.x + 1, self.y
		elif self.rotation == Orientation.DU:
			return self.x, self.y - 1
		elif self.rotation == Orientation.RL:
			return self.x, self.y
		elif self.rotation == Orientation.UD:
			return self.x, self.y

	def __str__(self):
		return View.render(self)

