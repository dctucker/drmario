import random

from cell import Cell
from pill import Pill

class Bottle:
	def __init__(self, other=None, width=8, height=16):
		self.width = width
		self.height = height
		if other is None:
			self.empty()
		else:
			self.cells = other.cells.copy()

	def __str__(self):
		return View.render(self)

	def empty(self):
		self.cells = [[Cell() for row in range(0,self.width)] for col in range(0,self.height)]
	
	def infect(self, count):
		while self.virus_count() < count:
			x = random.randint(0, self.width-1)
			y = random.randint(4, self.height-1)
			cell = self.cell_at(x, y)
			cell.infect()
	
	def drop_pill(self, pill):
		pill.x = int(self.width / 2) - 1
		pill.y = 1
		x1,y1,x2,y2 = pill.coords()
		cell1 = self.cell_at(x1, y1)
		cell2 = self.cell_at(x2, y2)
		if cell1.is_empty() and cell2.is_empty():
			self.format_pill(pill)
			return True
		else:
			return False
	
	def format_pill(self, pill):
		x1,y1,x2,y2 = pill.coords()
		pcell1 = self.cell_at(x1,y1)
		pcell2 = self.cell_at(x2,y2)
		if x1 < x2:
			pill.bind_rtl()
		elif x1 > x2:
			pill.bind_ltr()
		else:
			pill.unbind()
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
	
	def virus_count(self):
		count = 0
		for i,row in enumerate(self.cells):
			for j,cell in enumerate(row):
				if cell.is_virus() and not cell.is_zapped():
					count += 1
		return count

	
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
		applied = 0
		for y in range(self.height-1, 0, -1):
			for x,cell in enumerate(self.cells[y]):
				if not cell.is_pill(): continue
				if cell.is_zapped(): continue
				if not cell.is_bound():
					below = self.cell_at(x,y+1)
					if below is None:
						continue
					if below.is_empty():
						self.cell_at(x, y+1).value = cell.value
						cell.empty()
						applied += 1
		return applied

	def zap_bound(self, x, y):
		cell = self.cell_at(x,y)
		if cell.is_bound_left():
			self.cell_at(x-1, y).unbind()
		if cell.is_bound_right():
			self.cell_at(x+1, y).unbind()
	
	def zap_aligned(self):
		zap = False
		for y,row in enumerate(self.cells):
			for x,cell in enumerate(row):
				if cell.is_virus() or cell.is_pill():
					color = cell.color()

					# vertical
					aligned = True
					for dy in range(1, 4):
						c = self.cell_at(x, y+dy)
						aligned = aligned and c and c.color() == color
					if aligned:
						for dy in range(0, 4):
							self.cell_at(x, y+dy).zap()
							self.zap_bound(x, y+dy)
						zap = True

					# horizontal
					aligned = True
					for dx in range(1, 4):
						c = self.cell_at(x+dx, y)
						aligned = aligned and c and c.color() == color
					if aligned:
						for dx in range(0, 4):
							self.cell_at(x+dx, y).zap()
							self.zap_bound(x+dx, y)
						zap = True
		return zap

	def clear_zapped(self):
		for y,row in enumerate(self.cells):
			for x,cell in enumerate(row):
				if cell.is_zapped():
					if cell.is_bound_left():
						self.cell_at(x-1, y).unbind()
					if cell.is_bound_right():
						self.cell_at(x+1, y).unbind()
					cell.empty()

class View:
	def bottle_top(bottle):
		ret = ""
		ret += " " + " " * bottle.width + "╥      ╥\n"
		top = ('═' * bottle.width * 1)
		ret += "╔%s╝      ╚%s╗" % (top,top)
		ret += "\n"
		return ret

	def render(bottle):
		ret = ""
		ret += View.bottle_top(bottle)
		rows = ["".join(str(c) for c in row) for row in bottle.cells]
		ret += "\n".join(("║%s\033[0m║" % row) for row in rows)
		ret += "\n"
		ret += "╚" + "═" * bottle.width * 3 + "╝"
		ret += "\n"
		return ret
