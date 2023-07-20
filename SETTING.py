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

#Size of cell and board for 7x7
CELL_SIZE = 80
BOARD_LENGTH = 7

# #Size of cell and board for 10x10
# CELL_SIZE = 50
# BOARD_LENGTH = 10

# #Size of cell and board for 6x6
# CELL_SIZE = 80
# BOARD_LENGTH = 6

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
MAP_PIECES = ["b-", "b0", "b1", "b2", "b3", "b4"]


#################### FOR HEURISTIC ####################
DIMENTION = BOARD_LENGTH
BULB = 8
EMPTY = -1
CROSS = -2
NONUMBER = 5
NUMBER0 = 0
NUMBER1 =1
NUMBER2 = 2
NUMBER3 = 3
NUMBER4 = 4
LIGHTED = [7,15,23]
CROSSLIGHT = [6,14,22]

TRANSLATE = {
    "--": EMPTY, "b-": NONUMBER, "b0": NUMBER0, "b1": NUMBER1, "b2": NUMBER2, "b3": NUMBER3, "b4": NUMBER4
}

DECODE = {
    EMPTY: "--", NONUMBER: "b-", NUMBER0: "b0", NUMBER1: "b1", NUMBER2: "b2", NUMBER3: "b3", NUMBER4: "b4"
}