#!/usr/bin/env python3
from game import Game
from term import Term

import time
ticked = 0

term = Term()
game = Game()
game.begin()
game.toss_pill()

def display():
	term.clear()
	print(game.display())

while True:
	key = term.getch()
	if key:
		if key == '\033[B':
			game.move_down()
		if key == '\033[D':
			game.move_left()
		if key == '\033[C':
			game.move_right()
		if key == 'z':
			game.rotate_pill(False)
		if key == 'x':
			game.rotate_pill(True)

		if key == 'q':
			break

		display()
	
	now = time.time()
	if now - ticked > 1:
		ticked = now
		game.tick()
		display()

	#if key.is_pressed('left'):
	#	game.move_left()
	#elif key.is_pressed('right'):
	#	game.move_right()
	#elif key.is_pressed('z'):
	#	game.rotate_pill(False)
	#elif key.is_pressed('x'):
	#	game.rotate_pill(True)
	#else:
	#	continue


#def main(win):
#	win.clear()
#
#	win.refresh()
#	game = Game()
#	game.begin()
#	win.addstr(game.display())
#	game.toss_pill()
#
#	win.nodelay(True)
#	key = None
#	win.addstr("Detected key:" + str(key))
#	while True:
#		key = win.getch()
#		game.display()
#		if key == ord('q'):
#			break
#	
#curses.wrapper(main)

