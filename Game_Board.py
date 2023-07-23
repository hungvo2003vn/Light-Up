from SETTING import *
import pygame as pg
from pygame.locals import *
import UI
import copy
import csv
import time
from TEST_CASE import *
from Map_generator import *
from Heuristic_Board import *

#################### CLASS BOARD ####################

class Board:

    def __init__(self, Font, input_name, random_size):

        # SIZE
        self.BOARD_LENGTH = None
        self.CELL_SIZE = None
        self.X_BOARD = 10
        self.Y_BOARD = None
        self.input_name = input_name
        self.random_size = random_size # IF input_name = '' the map will be randomly genarated by the generator follow the size
        # MAP
        self.BOARD = None
        self.PIECES_MAP = None
        self.AI_MAP = None
        self.TESTING_MAP = None
        # MODE
        self.user = None
        self.ai_turn = False
        # Font
        self.Font = Font
        # Move Logs
        self.User_move_logs = []
        self.AI_move_logs = []

        # For AI's solver
        self.Solutions_Xcross = []
        self.solved = False
        self.found_solution = False
        self.Solutions = []

        # For DFS
        self.Black_cells = []
        self.White_cells = []
        self.num_v = 0
        self.branch = 0
        self.all_path_traversed = ''

        self.DFS_solved = False
        self.DFS_found_solution = False
        self.DFS_Solutions = []
        self.DFS_turn = False

        # For Heuristic
        self.Heu_solved = False
        self.Heu_found_solution = False
        self.Heu_Solutions = []
        self.Heu_turn = False
    
    def reset(self):
        self.__init__(self.Font, self.input_name, self.random_size)

    def adjust_constant(self, size):

        self.BOARD_LENGTH = size
        if size == 7:
            self.CELL_SIZE = 80
        elif size == 10:
            self.CELL_SIZE = 50
        elif size == 14:
            self.CELL_SIZE = 40
        self.Y_BOARD = (SCREEN_HEIGHT - self.CELL_SIZE * self.BOARD_LENGTH)/2

        return
    def get_output_name(self):
        if self.input_name == 'random':
            return f'-random_size{self.random_size}x{self.random_size}.txt'
        return '-'+self.input_name+'.txt'

    def make_board(self, display_screen):

        # Draw board
        self.BOARD = pg.surface.Surface((self.CELL_SIZE * self.BOARD_LENGTH, self.CELL_SIZE * self.BOARD_LENGTH))
        self.BOARD.fill(WHITE)

        display_screen.blit(self.BOARD, (self.X_BOARD, self.Y_BOARD))

        return

    def make_map(self):

        if self.PIECES_MAP is not None:
            return
        
        # LIST_TESTS_10x10 = [TEST5, TEST6]
        # LIST_TESTS_7x7 = [self.map_creation(size = 7), TEST1, TEST2, TEST3, TEST4]
        # LIST_TESTS_7x7 = [self.map_creation(size = 7)]
        # TEST = LIST_TESTS_7x7[0]

        TEST = None
        if self.input_name == 'random':
            TEST = self.map_creation(size = self.random_size)
        else:
            TEST = self.read_input(input_name=self.input_name, decode=True)

        self.adjust_constant(size = len(TEST))

        self.PIECES_MAP = copy.deepcopy(TEST)
        self.AI_MAP = copy.deepcopy(TEST)
        self.TESTING_MAP = copy.deepcopy(TEST)

        # Creating Cell object for each coordinate
        for y in range(self.BOARD_LENGTH):
            for x in range(self.BOARD_LENGTH):
                self.PIECES_MAP[y][x] = Cell(y, x, TEST[y][x])
                self.AI_MAP[y][x] = Cell(y, x, TEST[y][x])

        # Add neighbor
        for y in range(self.BOARD_LENGTH):
            for x in range(self.BOARD_LENGTH):

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

        # Split Black_cells and valid White_cells
        self.ai_turn = True
        self.collect_Black_White_cells()
        self.ai_turn = False

        return
    
    def load_pieces_img(self):

        PIECES_IMG = {}

        for pieces in PIECES:
            PIECES_IMG[pieces] = pg.image.load("img/"+ pieces + ".png")
            PIECES_IMG[pieces] =pg.transform.scale(PIECES_IMG[pieces], (self.CELL_SIZE*0.5, self.CELL_SIZE*0.5))

        return PIECES_IMG
    
    def load_pieces_map(self, display_screen):

        # Load img of some pieces
        PIECES_IMG = self.load_pieces_img()

        for y in range(0, self.BOARD_LENGTH):
            for x in range(0, self.BOARD_LENGTH):

                pieces = self.get_value(y, x).value

                x_pos = x*self.CELL_SIZE + self.X_BOARD
                y_pos = y*self.CELL_SIZE + self.Y_BOARD

                # This cell is lighting
                if pieces[0] == 'f':

                    # Highligt background
                    pg.draw.rect(display_screen, GREEN_YELLOW, (x_pos,  y_pos, self.CELL_SIZE, self.CELL_SIZE))

                    # Load the light bulb if this cell has it
                    if pieces == "fr" or pieces == "fw":
                        display_screen.blit(PIECES_IMG[pieces], (x_pos + self.CELL_SIZE//4, y_pos + self.CELL_SIZE//4, self.CELL_SIZE, self.CELL_SIZE))
                
                # This is a black cell
                elif pieces[0] == 'b':

                    content = pieces[1]
                    # Adjust content if this cell is a special black cell "b-"
                    if content == '-':
                        content = ""

                    # Draw black cell
                    UI.CreateButton(display_screen, x_pos, y_pos, self.CELL_SIZE, self.CELL_SIZE, content, self.Font[1], WHITE, BROWN)
                
                # Highlight marked cell
                if pieces[1] == 'x':

                    UI.CreateTitle(display_screen, x_pos + self.CELL_SIZE//2, y_pos + self.CELL_SIZE//2, 'X', self.Font[1], RED)
                    

                
                # Draw frame for each cell
                pg.draw.rect(display_screen, LIGHT_BROWN, (x_pos,  y_pos, self.CELL_SIZE, self.CELL_SIZE), 1 )
                
        return
    
    def make_board_all(self, display_screen):

        self.make_map()
        self.make_board(display_screen)
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

        for i in range(1, self.BOARD_LENGTH):

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
        return (x in range(0, self.BOARD_LENGTH) and y in range(0, self.BOARD_LENGTH))
    
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
        
        # Add to move_log
        self.add_logs(pos=Move, value_1=current_piece.value[1], type=type)

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

        start_col = (int)((pos[0] - self.X_BOARD) // self.CELL_SIZE)
        start_row = (int)((pos[1] - self.Y_BOARD) // self.CELL_SIZE)

        if self.valid_click(start_row, start_col):
            self.make_move([start_row, start_col], type)
        print([start_row, start_col])
        return
    
    def clear_moves(self):

        move_logs = None
        if self.ai_turn:
            move_logs = self.AI_move_logs
        else:
            move_logs = self.User_move_logs
        
        while len(move_logs) > 0:
            self.undo_move()
        
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
        elif not right_neighbor:
            message = "Wrong num of neighbors!"
        elif not all_fill:
            message = "Missed lights!"
        
        game_over = valid and all_fill and right_neighbor

        return game_over, message

    ################ Undo Move ################
    def add_logs(self, pos, value_1, type):
        if self.ai_turn:
            self.AI_move_logs += [[pos, [value_1, type]]]
        else:
            self.User_move_logs += [[pos, [value_1, type]]]
        return
    
    def undo_move(self):

        latest_move = None
        move_logs = None

        if self.ai_turn:
            move_logs = self.AI_move_logs
        else:
            move_logs = self.User_move_logs
            
        # If move_log is None
        if len(move_logs) == 0:
            return
        
        # Get latest move
        latest_move = move_logs.pop()

        # Get all value from latest move
        pos = latest_move[0]
        value_1 = latest_move[1][0]
        type_click = latest_move[1][1]

        # Undo Move
        self.make_move(Move=pos, type=type_click)
        move_logs.pop()

        if value_1 != '-':
            if value_1 == 'x':
                undo_type_click = RIGHT
            else:
                undo_type_click = LEFT

            if undo_type_click != type_click:
                self.make_move(Move=pos, type=undo_type_click)
                move_logs.pop()

        return
    
    ###################### For AI solver ######################
    def collect_Black_White_cells(self):
        
        # Collect
        for row in self.AI_MAP:
            for cell in row:
                if cell.value[0] == 'b':
                    self.Black_cells.append(cell)
                else:
                    self.White_cells.append(cell)
        
        # Filter White_cells
        for cell in self.Black_cells:

            # 0 light around
            if cell.value[1] == '0':

                for neighbor in cell.neighbors:
                    
                    # Marked as X
                    if neighbor.value == '--' or neighbor.value == 'f-':
                        
                        # Add to Xcross solution
                        if neighbor.pos not in self.Solutions_Xcross:
                            self.Solutions_Xcross.append(neighbor.pos)

                    # All the neighbor cell will be removed from the white list
                    # Remove 
                    try:
                        self.White_cells.remove(neighbor)
                    except ValueError:
                        pass

            
            elif cell.static_black_cell():

                for neighbor in cell.neighbors:
                    
                    if neighbor.value == '--':
                        
                        self.make_move(neighbor.pos, LEFT) # Make move
                        self.DFS_Solutions.append(neighbor.pos) # Add to solution

                        # All the neighbor cell will be removed from the white list
                        possible_hl = self.possible_highlight(neighbor.pos)
                        for pos in possible_hl:
                            illuminated_cell = self.get_value(pos[0], pos[1])
                            # Remove 
                            try:
                                self.White_cells.remove(illuminated_cell)
                            except ValueError:
                                pass

                    # Remove
                    try:
                        self.White_cells.remove(neighbor)
                    except ValueError:
                        pass
        return
    
    def AI_solver(self):
        
        # Undo some moves to clear the board
        while len(self.AI_move_logs) > 0:
            self.undo_move()
        
        # Make some initial moves
        for pos in self.DFS_Solutions:
            self.make_move(pos, LEFT)

        game_over, message = self.is_over()
        if not game_over and message == "Overlap detected!":
            self.solved = True
            return False

        vertex = []
        temporary_solution = []

        # Get all valid vertex
        for cell in self.White_cells:
            vertex.append(cell)

        # Start searching
        found_solution = self.DFS(vertex, temporary_solution)
        self.found_solution = found_solution # Global found
        self.DFS_found_solution = found_solution

        # Append solution
        self.DFS_Solutions += temporary_solution
        self.Solutions = []
        self.Solutions += self.DFS_Solutions # Global solution

        # Mark as solved
        self.solved = True # Global solved
        self.DFS_solved = True

        # Undo some moves to clear the board
        while len(self.AI_move_logs) > 0:
            self.undo_move()

        return found_solution
    
    def DFS_solver(self):

        start_time = time.time()
        found_solution = self.AI_solver()
        end_time = time.time() - start_time

        output_name = self.get_output_name()
        file_out = open(f"./output/DFS{output_name}", "w")

        finished_string = ''
        finished_string += f'---------Time elapsed: {end_time}---------\n'

        if found_solution:

            all_path_string = ''

            # Append Xcross Solutions
            cros_path = self.Solutions_Xcross
            if len(cros_path) > 0:

                all_path_string += 'Set Cross: '
                path_string = ''
                for step in cros_path:
                    step_str = ', '.join(str(coord) for coord in step)
                    step_str = f'({step_str})'
                    path_string += step_str + ', '
                
                path_string = path_string[:-2]
                path_string = f'[{path_string}]\n'

                all_path_string += path_string

            # Append Solutions
            lights_path = self.Solutions
            all_path_string += 'Set Lights: '
            path_string = ''
            for step in lights_path:
                step_str = ', '.join(str(coord) for coord in step)
                step_str = f'({step_str})'
                path_string += step_str + ', '
            
            path_string = path_string[:-2]
            path_string = f'[{path_string}]'
            all_path_string += path_string

            # Append all
            finished_string += all_path_string

        else:
            finished_string += 'No Solution!'

        finished_string += f'\nNumber of vertexes in Tree: {len(self.White_cells)}\n'
        finished_string += f"Number of visited vertexes: {self.num_v}"
        print(finished_string)
        file_out.write(self.all_path_traversed + finished_string)
        file_out.close()

        return found_solution
    
    def Heuristic_Solver(self):
        
        # Undo some moves to clear the board
        while len(self.AI_move_logs) > 0:
            self.undo_move()

        Cc = 7
        Pp = 0.37
        numberiterator = 100000
        
        # Convert to number map
        state = self.convert_testing_map()
        boardFirst = HBoard(state)
        
        # Init Problem
        s = problem(boardFirst, Cc,Pp,numberiterator)
        boardFirst = s.prepareToSearch(boardFirst) # Fix the bug
        s.start = deepcopy(boardFirst)
        s.goal = deepcopy(boardFirst)
        
        # Start simulating
        startTime = time.time()
        solution = simulated_annealing(s, numberiterator)
        endTime = time.time() - startTime

        ################## WRITE TO FILE ##################
        output_name = self.get_output_name()
        file_out = open(f"./output/Heuristic{output_name}", "w")

        for j in range(len(solution)):
            for i in range(DIMENTION):

                board_row_str = ', '.join(str(cell) for cell in solution[j].board[i])
                board_row_str = f'[{board_row_str}]\n'
                file_out.write(board_row_str)

            file_out.write(f'-------{solution[j].score}--------\n')

        file_out.write(f'time elapsed: {endTime}\n')
        file_out.write('Solution: ')

        path_string = ''
        path = []
        if len(solution) > 0:
            # path = solution[-1].numberBulb
            solution_board = solution[-1].board
            for r in range(len(solution_board)):
                for c in range(len(solution_board)):
                    if solution_board[r][c]  == 8:
                        path.append((r, c))
        # path = self.make_unique(path_list = path)

        new_path = []
        for step in path:
            new_path.append([step[0], step[1]])
            step_str = ', '.join(str(coord) for coord in step)
            step_str = f'({step_str})'
            path_string += step_str + ', '
        
        path_string = path_string[:-2]
        file_out.write(f'[{path_string}]')
        file_out.close()
        ###################################################

        print('time elapsed', endTime)
        print('Solution:\n', path)

        ############## Update some attributes #############
        self.Heu_found_solution = solution[-1].checkEnd()
        self.Heu_solved = True
        self.Heu_Solutions += new_path

        self.Solutions = []
        self.Solutions += self.Heu_Solutions
        self.found_solution = self.Heu_found_solution
        self.solved = self.Heu_solved

        ###################################################
        while len(self.AI_move_logs) > 0:
            self.undo_move()
        
        boardFirst = None
        s = None

        return self.Heu_found_solution
    
    def DFS(self, vertex, temporary_solution, level = 0):

        if level >= len(vertex):
            game_over, mess = self.is_over()
            self.branch += 1

            ######### WRITE SOLUTION#########
            currnet_map = self.print_map()
            solving_string = f'############# Path branch: {self.branch} #############\n'
            solving_string += currnet_map
            solving_string += f'---------Game Over: {game_over}, Message: {mess}---------'
            ##########################################
            print(solving_string)
            self.all_path_traversed += solving_string + '\n'

            return game_over
        
        # Increase num_v
        self.num_v +=1 
        # Get node of this level
        top = vertex[level]

        if not top.illuminated:
            
            # Place light at this pos (Visited = True)
            self.make_move(top.pos, LEFT)
            temporary_solution.append(top.pos)

            # Do the DFS search
            valid = self.DFS(vertex, temporary_solution, level + 1)
            
            # Undo visit (Visited = False)
            self.undo_move()

            # If solution was found
            if valid:
                return True
            else:
                temporary_solution.remove(top.pos)

        # Not placing a light
        return self.DFS(vertex, temporary_solution, level + 1)

    ###################### MAP GENERATOR ######################
    def map_creation(self, size):

        My_map = map_generator(size)
        grid = My_map.map_generation()
        My_map.print_map()
        
        return grid
    
    def print_map(self):

        curent_map = ''
        for row in self.AI_MAP:
            new_row = []
            for cell in row:
                new_row.append(cell.value)
            curent_map += '[' + ', '.join(new_row) + ']\n'

        return curent_map
    
    def convert_testing_map(self):

        translate_map = copy.deepcopy(self.TESTING_MAP)
        size = len(translate_map)

        for row in range(size):
            for col in range(size):
                cell = translate_map[row][col]
                translate_map[row][col] = TRANSLATE[cell]

        return translate_map
    
    def read_input(self, input_name, decode = False):

        board=[]
        with open(f'./input/{input_name}.csv', newline='') as csvfile:

            csvreader = csv.reader(csvfile, delimiter=',')

            for row in csvreader:
                intRow = [int(element) for element in row]
                board += [intRow]
        
        # Converting map to string
        if decode:
            for row in range(len(board)):
                for col in range(len(board)):
                    cell = board[row][col]
                    board[row][col] = DECODE[cell]

        return board
    
    def make_unique(self, path_list):
        path = []
        for pos in path_list:
            if pos not in path:
                path.append(pos)

        return path
        


# Init map
# game = Board([])
# game.make_map()
# game.ai_turn = True
# print(game.Heuristic_Solver())
# game.DFS_solver()







    
