from SETTING import *
import pygame as pg
from pygame.locals import *
import UI
import copy
import random
from TEST_CASE import *
from Cell_Board import *

#################### CLASS BOARD ####################

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
        self.PIECES_MAP = copy.deepcopy(TEST)
        self.AI_MAP = copy.deepcopy(TEST)

        # Creating Cell object for each coordinate
        for y in range(BOARD_LENGTH):
            for x in range(BOARD_LENGTH):
                self.PIECES_MAP[y][x] = Cell(y, x, TEST[y][x])
                self.AI_MAP[y][x] = Cell(y, x, TEST[y][x])

        # Add neighbor
        for y in range(BOARD_LENGTH):
            for x in range(BOARD_LENGTH):

                user_cell = self.PIECES_MAP[y][x]
                ai_cell = self.AI_MAP[y][x]

                up = [y - 1, x]
                down = [y + 1, x]
                left = [y, x - 1]
                right = [y, x + 1]
                directions = [up, down, left, right]

                for pos in directions:
                    row, col = pos[0], pos[1]

                    if self.inside_click(row, col):
                        user_neighbor = self.PIECES_MAP[row][col]
                        ai_neighbor = self.AI_MAP[row][col]

                        user_cell.add_neighbor(user_neighbor)
                        ai_cell.add_neighbor(ai_neighbor)

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

                pieces = self.get_value(y, x).value

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

        cell = self.get_value(row, col)
        cell.value = value

        return

    def set_illu(self, row, col, cell, turn_on):

        if turn_on:

            if self.ai_turn:
                self.AI_MAP[row][col].set_illuminated(cell)
            else:
                self.PIECES_MAP[row][col].set_illuminated(cell)
        else:
            if self.ai_turn:
                self.AI_MAP[row][col].reset_illuminated(cell)
            else:
                self.PIECES_MAP[row][col].reset_illuminated(cell)
        return
    
    def same_pos(self, source, des):
        return source[0] == des[0] and source[1] == des[1]

    def possible_highlight(self, pos):

        able_moving = [True for i in range(4)]
        row, col = pos[0], pos[1]

        possible_hl = [[row, col]]

        for i in range(1, BOARD_LENGTH):

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

        piece = self.get_value(row, col).value

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
        if current_piece.value == "fw" or current_piece.value == "fr":
            turn_on = False
        elif type == LEFT:
            turn_on = True
        
        # Toggle Marking X
        if turn_on is None:
            if current_piece.value[1] == '-':
                self.set_value(row, col, current_piece.value[0] + 'x')
            else:
                self.set_value(row, col, current_piece.value[0] + '-')

        else:

            possible_hl = self.possible_highlight(Move)

            for pos in possible_hl:
                
                piece = self.get_value(pos[0], pos[1])

                self.set_illu(pos[0], pos[1], current_piece, turn_on)

                # No matter whether this cell is turn off or not we still mark the X if the type is RIGHT clicked
                if type == RIGHT and self.same_pos(pos, Move):
                    self.set_value(pos[0], pos[1], piece.value[0] + 'x')


        return

    def checking_clicked(self, pos, type):

        start_col = (int)((pos[0] - X_BOARD) // CELL_SIZE)
        start_row = (int)((pos[1] - Y_BOARD) // CELL_SIZE)

        if self.valid_click(start_row, start_col):

            self.make_move([start_row, start_col], type)
        print([start_row, start_col])
        return
    
    ################ CHECKING VICTORY ################
    def is_over(self):

        MAP = None
        if self.ai_turn:
            MAP = self.AI_MAP
        else:
            MAP = self.PIECES_MAP
        
        all_fill = True
        valid = True
        right_neighbor = True
        game_over = False

        for row in MAP:
            for ele in row:

                if ele.value[0] == 'b':
                    need, count = ele.num_neighbor_lights()
                    if need != None and need != "Any":
                        if need != count:
                            right_neighbor = False

                if ele.value[0] == '-':
                    all_fill = False

                if ele.value[1] == 'w':
                    valid = False

        message = "Valid Solution"
        if not valid:
            message = "Overlap detected!"
        elif not all_fill:
            message = "Missed lights!"
        elif not right_neighbor:
            message = "Wrong num of neighbors!"
        
        game_over = valid and all_fill and right_neighbor

        return game_over, message

    





    
