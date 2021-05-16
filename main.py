#!/usr/bin/env python3
from game import Game
from term import Term

KEY_LEFT = '\033[D'
KEY_RIGHT = '\033[C'
KEY_DOWN = '\033[B'

term = Term()
game = Game(10, 0)
game.begin()
game.toss_pill()

def display():
	term.clear()
	print(str(game))

while True:
	key = term.getch()
	if key:
		if key == KEY_DOWN:
			game.move_down()
		if key == KEY_LEFT:
			game.move_left()
		if key == KEY_RIGHT:
			game.move_right()
		if key == 'z':
			game.rotate_pill(False)
		if key == 'x':
			game.rotate_pill(True)

		if key in  ('q', '\033'):
			break

		display()
	
	if game.tick():
		display()

	if game.win():
		print("YOU WIN!")
		break
	if game.lose():
		print("YOU LOSE")
		break

