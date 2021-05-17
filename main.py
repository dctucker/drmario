#!/usr/bin/env python3
from game import Game
from term import Term

term = Term()
game = Game(10, 0)
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

