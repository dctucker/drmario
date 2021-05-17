
class Game:
	def render(game):
		next_pill = " " * game.bottle.width * 2 + "   " + str(game.next_pill)
		bottle = "\n     ".join( game.bottle.lines() )
		stats = ""
		stats += "PILL " if game.pill is not None else "     "
		stats += "STATE: %d " % game.state
		stats += "VIRUS: %d " % game.bottle.virus_count()
		stats += "COMBO: %d " % game.combo
		return "     %s\n     %s\n%s" % (next_pill, bottle, stats)

class Bottle:
	def bottle_top(bottle):
		spaces = " " * bottle.width
		top = '═' * bottle.width * 1
		return [
			" %s╥      ╥%s " % (spaces, spaces),
			"╔%s╝      ╚%s╗" % (top,top),
		]

	def lines(bottle):
		rows = ["".join(str(c) for c in row) for row in bottle.cells]
		cells = [("║%s\033[0m║" % row) for row in rows]
		return [] + Bottle.bottle_top(bottle) + cells + [
			"╚" + "═" * bottle.width * 3 + "╝",
		]

	def render(bottle):
		return "\n".join(Bottle.lines(bottle)) + "\n"

class Cell:
	def ansi_color(cell):
		return {
			cell.RED: "\033[0;30;41;4m",
			cell.YELLOW: "\033[0;30;43;4m",
			cell.BLUE: "\033[0;30;46;4m",
			cell.EMPTY: "\033[0;34;40m",
		}[cell.color()]

	def color_str(cell):
		return {
			cell.RED: "▌Ѧ▐",
			cell.YELLOW: "▌Ѡ▐",
			cell.BLUE: "▌Ж▐",
			cell.EMPTY: "   ",
		}[cell.color()]

	def render(cell):
		a = Cell.ansi_color(cell)
		c = Cell.color_str(cell)
		if cell.is_zapped():
			c = "\033[24;7m<◙>\033[27m"
		elif cell.is_pill():
			c = " "
			if cell.is_bound_left():
				c = " %s▐" % c
			elif cell.is_bound_right():
				c = "▌%s " % c
			else:
				c = "▌%s▐" % c
		return "%s%s" % (a, c)

class Pill:
	def render(pill):
		return str(pill.cell1) + str(pill.cell2) + "\033[0m"

