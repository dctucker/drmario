#!/usr/bin/env python3
import sys

from enums import Speed
from game import Game
from term import Term

def usage(name):
	print(f"Usage: {name} <level> <speed>")
	print("\tlevel is 1 to 20, default 10")
	print("\tspeed is 0/1/2 for low/med/high, default 1")
	print()
	print("\tControls: left/right/down moves, z/x rotates")

def main(args):
	def arg(i, default=None):
		if len(args) > i:
			return args[i]
		return default

	if arg(1) in ('--help', '-h'):
		usage(arg(0))
		return
	level = int(arg(1, 10))
	speed = int(arg(2, Speed.LOW))

	term = Term()
	game = Game(level, speed)
	game.begin()
	game.toss_pill()

	keymap = {
		Term.KEY_DOWN: 'move_down',
		Term.KEY_LEFT: 'move_left',
		Term.KEY_RIGHT:'move_right',
		('z',): 'rotate_pill_back',
		('x',): 'rotate_pill',
		(' ',): 'slam_pill',
		('p',): 'toggle_pause',
		('q','\033'): 'quit',
	}

	while True:
		key = term.getch()
		if key:
			if game.is_paused():
				game.toggle_pause()
				continue
			for keys, action in keymap.items():
				if key in keys:
					getattr(game, action)()
					break

			term.display(game)
		
		if game.tick():
			term.display(game)

		if game.win():
			print("YOU WIN!")
			break
		if game.lose():
			print("YOU LOSE")
			break
		if game.has_quit():
			print("BYE")
			break

if __name__ == '__main__':
	main(sys.argv)
