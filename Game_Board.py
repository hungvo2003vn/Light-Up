from SETTING import *
import pygame as pg
from pygame.locals import *
import UI
import copy
import random
from TEST_CASE import *

class Board:

    def __init__(self, Font):

        self.BOARD = None
        self.PIECES_MAP = None
        self.AI_MAP = None

        self.user = None
        self.ai_turn = False

        self.Font = Font

        self.Lighting = []
        self.Move_logs = []
    
    def make_board(self, display_screen):

        # Draw board
        self.BOARD = pg.surface.Surface((CELL_SIZE * BOARD_LENGTH, CELL_SIZE * BOARD_LENGTH))
        self.BOARD.fill(WHITE)

        display_screen.blit(self.BOARD, (X_BOARD, Y_BOARD))

        return

    def make_map(self):

        if self.PIECES_MAP is not None:
            return
        
        TEST = copy.deepcopy(TEST1)
        self.PIECES_MAP = TEST
        self.AI_MAP = copy.deepcopy(TEST)

        # Randomly map creation
        # TODO
        # Your Code here

        return
    
    def load_pieces_img(self):

        PIECES_IMG = {}

        for pieces in PIECES:
            PIECES_IMG[pieces] = pg.image.load("img/"+ pieces + ".png")
            PIECES_IMG[pieces] =pg.transform.scale(PIECES_IMG[pieces], (CELL_SIZE*0.5, CELL_SIZE*0.5))

        return PIECES_IMG
    
    def load_pieces_map(self, display_screen):

        # Load img of some pieces
        PIECES_IMG = self.load_pieces_img()

        for y in range(0, BOARD_LENGTH):
            for x in range(0,BOARD_LENGTH):

                pieces = self.get_value(y, x)

                x_pos = x*CELL_SIZE + X_BOARD
                y_pos = y*CELL_SIZE + Y_BOARD

                # This cell is lighting
                if pieces[0] == 'f':

                    # Highligt background
                    pg.draw.rect(display_screen, GREEN_YELLOW, (x_pos,  y_pos, CELL_SIZE, CELL_SIZE))

                    # Load the light bulb if this cell has it
                    if pieces == "fr" or pieces == "fw":
                        display_screen.blit(PIECES_IMG[pieces], (x_pos + CELL_SIZE//4, y_pos + CELL_SIZE//4, CELL_SIZE, CELL_SIZE))
                
                # This is a black cell
                elif pieces[0] == 'b':

                    content = pieces[1]
                    # Adjust content if this cell is a special black cell "b-"
                    if content == '-':
                        content = ""

                    # Draw black cell
                    UI.CreateButton(display_screen, x_pos, y_pos, CELL_SIZE, CELL_SIZE, content, self.Font[1], WHITE, BROWN)
                
                # Highlight marked cell
                if pieces[1] == 'x':

                    UI.CreateTitle(display_screen, x_pos + CELL_SIZE//2, y_pos + CELL_SIZE//2, 'X', self.Font[1], RED)
                    

                
                # Draw frame for each cell
                pg.draw.rect(display_screen, LIGHT_BROWN, (x_pos,  y_pos, CELL_SIZE, CELL_SIZE), 1 )
                
        return
    
    def make_board_all(self, display_screen):

        self.make_board(display_screen)
        self.make_map()
        self.load_pieces_map(display_screen)

        return

    ############# Making Move #############

    def get_value(self, row, col):

        if self.ai_turn:
            return self.AI_MAP[row][col]
        
        return self.PIECES_MAP[row][col]
    
    def set_value(self, row, col, value):

        if self.ai_turn:
            self.AI_MAP[row][col] = value
        
        else:
            self.PIECES_MAP[row][col] = value
        
        return
    
    def same_pos(self, source, des):
        return source[0] == des[0] and source[1] == des[1]

    def possible_highlight(self, pos):

        able_moving = [True for i in range(4)]
        row, col = pos[0], pos[1]

        possible_hl = []

        for i in range(0, BOARD_LENGTH):

            up = [row - i, col]
            down = [row + i, col]
            left = [row, col - i]
            right = [row, col + i]

            directions = [up, down, left, right]
            for index in range(len(directions)):

                position = directions[index]
                if self.valid_click(position[0], position[1]) and able_moving[index]:
                    possible_hl += [position]
                else:
                    able_moving[index] = False

        return copy.deepcopy(possible_hl)

    
    def inside_click(self, x, y):
        return (x in range(0, BOARD_LENGTH) and y in range(0, BOARD_LENGTH))
    
    def valid_click(self, row, col):

        # This click is not inside the board
        if not self.inside_click(row, col):
            return False

        piece = None
        if self.ai_turn:
            piece = self.AI_MAP[row][col]
        else:
            piece = self.PIECES_MAP[row][col]

        # This cell is black
        if piece[0] == 'b':
            return False
        
        return True

    ################ MAKE MOVE FUNCTION ################
    def make_move(self, Move, type):

        row, col = Move[0], Move[1]
        current_piece = self.get_value(row, col)
        turn_on = None

        # Figure out cases
        if current_piece == "fw" or current_piece == "fr":
            turn_on = False
        elif type == LEFT:
            turn_on = True
        
        # Toggle Marking X
        if turn_on is None:
            if current_piece[1] == '-':
                self.set_value(row, col, current_piece[0] + 'x')
            else:
                self.set_value(row, col, current_piece[0] + '-')

        else:

            possible_hl = self.possible_highlight(Move)

            for pos in possible_hl:
                
                piece = self.get_value(pos[0], pos[1])

                if turn_on:
                    
                    # If this is the choosen cell -> this will be a light
                    if self.same_pos(pos, [row, col]):
                        self.set_value(pos[0], pos[1], 'f' + 'r')

                    # This cell is illuminated by other
                    else:
                        self.set_value(pos[0], pos[1], 'f' + piece[1])

                    self.Lighting += [pos]

                else:

                    # Try to remove the cell illuminated by other light
                    try:
                        self.Lighting.remove(pos)
                    except ValueError:
                        pass
                    
                    # If choosen cell is a light bulb -> delete the light first
                    if self.same_pos(pos, [row, col]):
                        self.set_value(pos[0], pos[1], piece[0] + '-')

                        # No matter whether this cell is turn off or not we still mark the X if the type is RIGHT clicked
                        if type == RIGHT:
                            self.set_value(pos[0], pos[1], piece[0] + 'x')

                    # If this cell is actually turn off
                    if pos not in self.Lighting:
                        self.set_value(pos[0], pos[1], '-' + piece[1])

        return

    def checking_clicked(self, pos, type):

        start_col = (int)((pos[0] - X_BOARD) // CELL_SIZE)
        start_row = (int)((pos[1] - Y_BOARD) // CELL_SIZE)

        if self.valid_click(start_row, start_col):

            self.make_move([start_row, start_col], type)

        return
    

#################### CLASS SQUARE ####################
class Cell:

    def __init__(self, row, col, value):
        
        self.neighbors = []
        self.visited = False
        self.value = value
        self.pos = [row, col]

        self.is_bulb = False

        # Only for White Cell
        self.illuminated = False
        self.source_illuminated = []

    def add_neighbor(self, other_square):
        self.neighbors += [other_square]
    
    def set_visited(self, bool):
        self.visited = bool
    
    def same_pos(self, des):
        return (self.pos[0] == des[0]) and (self.pos[1] == des[1])
    
    # Only for White Cell
    def set_illuminated(self, cell):

        self.illuminated = True
        self.source_illuminated += [cell]

        # Change value
        self.value = 'f' +  self.value[1]

        # This is the case setting a light up
        if self.same_pos(cell.pos):

            self.is_bulb = True
            if self.is_overlap():
                self.value = "fw"
            else:
                self.value = "fr"
        return

    def is_overlap(self):

        if self.is_bulb and len(self.source_illuminated) > 1:
            return True
        return False

    # Remember the X case
    def reset_illuminated(self, cell):

        try:
            self.source_illuminated.remove(cell)
        except ValueError:
            pass

        # Remove all
        if self.source_illuminated == []:

            self.source_illuminated = False
            self.value = '-' +  self.value[1]

        # Toggle itself
        if self.same_pos(cell.pos):

            self.is_bulb = False
            self.value = "--" # Remember the X case will be "-x"
        
        return len(self.source_illuminated) == 0



    
