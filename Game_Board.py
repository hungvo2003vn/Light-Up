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
        
        #self.PIECES_MAP = [[random.choice(ALL_PIECES) for x in range(0, BOARD_LENGTH)] for y in range(0, BOARD_LENGTH)]
        self.PIECES_MAP = copy.deepcopy(TEST1)

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

                pieces = self.PIECES_MAP[y][x]
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
    def make_move(self, Move, type):

        row, col = Move[0], Move[1]
        current_piece = self.PIECES_MAP[row][col]
        turn_on = None

        # Figure out cases
        if current_piece == "fw" or current_piece == "fr":
            turn_on = False
        elif type == LEFT:
            turn_on = True
        
        # Toggle Marking X
        if turn_on is None:
            if current_piece[1] == '-':
                self.PIECES_MAP[row][col] = current_piece[0] + 'x'
            else:
                self.PIECES_MAP[row][col] = current_piece[0] + '-'

        else:

            possible_hl = self.possible_highlight(Move)

            for pos in possible_hl:
                
                piece = self.PIECES_MAP[pos[0]][pos[1]]
                if turn_on:
                    if pos[0] == row and pos[1] == col:
                        self.PIECES_MAP[pos[0]][pos[1]] = 'f' + 'r'
                    else:
                        self.PIECES_MAP[pos[0]][pos[1]] = 'f' + piece[1]
                    self.Lighting += [pos]
                else:

                    try:
                        self.Lighting.remove(pos)
                    except ValueError:
                        pass

                    if pos not in self.Lighting:
                        self.PIECES_MAP[pos[0]][pos[1]] = '-' + piece[1]

                    if type == RIGHT and pos[0] == row and pos[1] == col:
                        self.PIECES_MAP[pos[0]][pos[1]] = piece[0] + 'x'

        return

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

        piece = self.PIECES_MAP[row][col]

        # This cell is black
        if piece[0] == 'b':
            return False
        
        return True


    def checking_clicked(self, pos, type):

        start_col = (int)((pos[0] - X_BOARD) // CELL_SIZE)
        start_row = (int)((pos[1] - Y_BOARD) // CELL_SIZE)

        if self.valid_click(start_row, start_col):

            self.make_move([start_row, start_col], type)

        return