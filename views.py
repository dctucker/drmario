from enums import Flags

class Game:
	def render(game):
		next_pill = ""
		bottle = ""
		stats = ""
		if game.is_paused():
			next_pill = "\033[J\033[H\n"
			bottle = "\n     ".join( Bottle.lines(game.bottle, empty=True) )
		else:
			next_pill = " " * game.bottle.width * 2 + "   " + str(game.next_pill)
			bottle = "\n     ".join( game.bottle.lines() )
		stats += "STATE: %s " % game.state.name
		stats += "COMBO: %d          \n" % game.combo
		stats += "VIRUS: %d " % game.bottle.virus_count()
		stats += "SPEED: %d " % game.speed
		stats += "LEVEL: %d " % game.level
		return "     %s\n     %s\n%s          " % (next_pill, bottle, stats)

class Bottle:
	def bottle_top(bottle):
		spaces = " " * bottle.width
		top = '═' * bottle.width * 1
		return [
			" %s╥      ╥%s " % (spaces, spaces),
			"╔%s╝      ╚%s╗" % (top,top),
		]

	def lines(bottle, empty=False):
		if empty:
			rows = ["".join("   " for c in row) for row in bottle.cells]
		else:
			rows = ["".join(str(c) for c in row) for row in bottle.cells]
		cells = [("║%s\033[0m║" % row) for row in rows]
		return [] + Bottle.bottle_top(bottle) + cells + [
			"╚" + "═" * bottle.width * 3 + "╝",
		]

	def render(bottle):
		return "\n".join(Bottle.lines(bottle)) + "\n"

class Cell:
	#LPAD = '▎'
	#RPAD = '▕'
	LPAD = '▌'
	RPAD = '▐'
	def ansi_color(cell):
		return {
			Flags.RED: "\033[0;30;41;4m",
			Flags.YELLOW: "\033[0;30;43;4m",
			Flags.BLUE: "\033[0;30;46;4m",
			Flags.EMPTY: "\033[0;34;40m",
		}[cell.color()]

	def color_str(cell):
		L,R = Cell.LPAD, Cell.RPAD
		return {
			Flags.RED: "%sѦ%s" % (L,R),
			Flags.YELLOW: "%sѠ%s" % (L,R),
			Flags.BLUE: "%sЖ%s" % (L,R),
			Flags.EMPTY: "   ",
		}[cell.color()]

	def render(cell):
		L,R = Cell.LPAD, Cell.RPAD
		a = Cell.ansi_color(cell)
		c = Cell.color_str(cell)
		if cell.is_zapped():
			c = "\033[24;7m<◙>\033[27m"
		elif cell.is_pill():
			c = " "
			if cell.is_bound_left():
				c = "╴" + c + R
			elif cell.is_bound_right():
				c = L + c + "╶"
			elif cell.is_bound_below():
				c = "\033[24m" + L + c + R
			else:
				c = L + c + R
		return "%s%s" % (a, c)

class Pill:
	def render(pill):
		return str(pill.cell1) + str(pill.cell2) + "\033[0m"

