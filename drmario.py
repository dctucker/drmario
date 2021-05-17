#!/usr/bin/env python3
import sys

from game import Game
from term import Term

def main(args):
	def arg(i, default=None):
		if len(args) > i:
			return args[i]
		return default

	if arg(1) in ('--help', '-h'):
		print(f"Usage: {arg(0)} <level> <speed>")
		print("\tlevel is 1 to 20, default 10")
		print("\tspeed is 0/1/2 for low/med/high, default 1")
		print()
		print("\tControls: left/right/down moves, z/x rotates")
		return
	level = int(arg(1, 10))
	speed = int(arg(2, 0))

	term = Term()
	game = Game(level, speed)
	game.begin()
	game.toss_pill()

	while True:
		key = term.getch()
		if key:
			if key in Term.KEY_DOWN:
				game.move_down()
			if key in Term.KEY_LEFT:
				game.move_left()
			if key in Term.KEY_RIGHT:
				game.move_right()
			if key == 'z':
				game.rotate_pill(False)
			if key == 'x':
				game.rotate_pill(True)
			if key == ' ':
				game.slam_pill()

			if key in ('q', '\033'):
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

if __name__ == '__main__':
	main(sys.argv)
