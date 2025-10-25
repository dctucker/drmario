"""provides constants used by the game logic"""

from enum import Enum, IntEnum, IntFlag

# Game
class State(Enum):
	"""game state constants"""
	MOVING = 0
	DROPPED = 1
	FALLING = 2
	NEW_PILL = 3
	WIN = 4
	LOSE = 5
	QUIT = 6
	PAUSED = 99

# Cell
class Flags(IntFlag):
	"""bits that describe board states"""
	#pylint: disable=implicit-flag-alias
	EMPTY = 0
	PILL = 1
	VIRUS = 2
	ZAP = 3
	RED = 4
	YELLOW = 8
	BLUE = 12
	BIND_NONE = 0
	BIND_LEFT = 16
	BIND_RIGHT = 32
	BIND_BELOW = 64

# Pill
class Orientation(IntEnum):
	"""describes pill rotation"""
	LR = 0
	DU = 1
	RL = 2
	UD = 3

class Speed(IntEnum):
	"""constants describing the game speed"""
	LOW = 0
	MED = 1
	HIGH = 2
