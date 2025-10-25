"""provides classes that enable viewing the game and its components"""

from enums import Flags

class Game:
	"""view of the game"""
	@staticmethod
	def render(game):
		"""return a string showing the entire game in its current state"""
		next_pill = ""
		bottle = ""
		stats = []
		if game.is_paused():
			next_pill = "\033[J\033[H\n"
			bottle = "\n     ".join( Bottle.lines(game.bottle, empty=True) )
		else:
			next_pill = " " * game.bottle.width * 2 + "   " + str(game.next_pill)
			bottle = "\n     ".join( game.bottle.lines() )
		stats = "".join([
			"STATE:", game.state.name, " ",
			"COMBO:", str(game.combo), "          \n",
			"VIRUS:", str(game.bottle.virus_count()), " ",
			"SPEED:", game.speed.name, " ",
			"LEVEL:", str(game.level), "\n",
			"SCORE:", str(game.score), " \n",
		])
		return "".join([
			"     ",
			next_pill,
			"\n     ",
			bottle,
			"\n",
			stats,
			"          "
		])

class Bottle:
	"""view of the bottle"""

	@staticmethod
	def bottle_top(bottle):
		"""return an array of strings representing the top part of the bottle"""
		spc = " " * bottle.width
		top = '═' * bottle.width * 1
		return [
			"".join([" ", spc, "╥      ╥", spc, " "]),
			"".join(["╔", top, "╝      ╚", top, "╗"]),
		]

	@staticmethod
	def lines(bottle, empty=False):
		"""return an array of strings representing the outline of the bottle"""
		if empty:
			rows = ["".join("   " for c in row) for row in bottle.cells]
		else:
			rows = ["".join(str(c) for c in row) for row in bottle.cells]
		cells = ["".join(["║", row, "\033[0m║"]) for row in rows]
		return [] + Bottle.bottle_top(bottle) + cells + [
			"╚" + "═" * bottle.width * 3 + "╝",
		]

	@staticmethod
	def render(bottle):
		"""return a string representing the entire bottle"""
		return "\n".join(Bottle.lines(bottle)) + "\n"

class Cell:
	"""view of a cell"""
	#LPAD = '▎'
	#RPAD = '▕'
	LPAD = '▌'
	RPAD = '▐'

	@staticmethod
	def ansi_color(cell):
		"""return an ANSI escape code for a given color"""
		return {
			Flags.RED    : "\033[0;30;41;4m",
			Flags.YELLOW : "\033[0;30;43;4m",
			Flags.BLUE   : "\033[0;30;46;4m",
			Flags.EMPTY  : "\033[0;34;40m",
		}[cell.color()]

	@staticmethod
	def color_str(cell):
		"""return a bare string representing the given cell"""
		l,r = Cell.LPAD, Cell.RPAD
		return {
			Flags.RED    : "".join([l, "Ѧ" , r]),
			Flags.YELLOW : "".join([l, "Ѡ" , r]),
			Flags.BLUE   : "".join([l, "Ж" , r]),
			Flags.EMPTY  : "   ",
		}[cell.color()]

	@staticmethod
	def render(cell):
		"""return a complete ANSI string for the given cell"""
		l,r = Cell.LPAD, Cell.RPAD
		a = Cell.ansi_color(cell)
		c = Cell.color_str(cell)
		if cell.is_zapped():
			c = "\033[24;7m<◙>\033[27m"
		elif cell.is_pill():
			c = " "
			if cell.is_bound_left():
				c = "╴" + c + r
			elif cell.is_bound_right():
				c = l + c + "╶"
			elif cell.is_bound_below():
				c = "\033[24m" + l + c + r
			else:
				c = l + c + r
		return "".join([a, c])

class Pill:
	"""view of a pill"""

	@staticmethod
	def render(pill):
		"""return a complete ANSI string representing the given pill"""
		return str(pill.cell1) + str(pill.cell2) + "\033[0m"
