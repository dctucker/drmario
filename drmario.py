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

keymap = {
	'move_down':    Term.KEY_DOWN,
	'move_left':    Term.KEY_LEFT,
	'move_right':   Term.KEY_RIGHT,
	'rotate_pill_back': ('z',),
	'rotate_pill':  ('x',),
	'slam_pill':    (' ',),
	'toggle_pause': ('p','\n'),
	'restart':      ('r',),
	'quit':         ('q','\033'),
}

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

	def check_actions(key, actions):
		for action in actions:
			if key in keymap[action]:
				getattr(game, action)()
				return True
		return False

	while not game.has_quit():
		key = term.getch()
		if key:
			if game.is_paused():
				check_actions(key, ('toggle_pause', 'quit', 'restart'))
			elif game.over():
				check_actions(key, ('quit', 'restart'))
			else:
				check_actions(key, keymap.keys())

			term.display(game)
		
		if game.tick():
			term.display(game)

if __name__ == '__main__':
	main(sys.argv)
