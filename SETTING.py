#Screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

#Set color with rgb
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
DIMGREY = (105,105,105)
BROWN = (192,192,164)
LIGHT_BROWN = (96,64,32)
GREEN_YELLOW = (173,255,47)

# Mouse event
LEFT = 1
RIGHT = 3

#Size of cell and board
CELL_SIZE = 80
BOARD_LENGTH = 7

#Board position
X_BOARD = (SCREEN_WIDTH - CELL_SIZE * BOARD_LENGTH)/2
X_BOARD = 10
Y_BOARD = (SCREEN_HEIGHT - CELL_SIZE * BOARD_LENGTH)/2

#Pieces
#Pieces name
# ["b-", "b0", "b1", "b2", "b3", "b4", "fr", "fw", "--", "f-", "-x", "fx"]
# bi: black cell with i bulbs surrounded
# _r/w: valid bulb or invalid bulb
# --: not filled cell
# f-: filled cell

PIECES = ["fr", "fw"]
ALL_PIECES = ["b-", "b0", "b1", "b2", "b3", "b4", "fr", "fw", "--", "f-", "-x", "fx"]
