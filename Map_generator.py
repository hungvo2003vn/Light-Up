import random
import copy
from Cell_Board import Cell

class map_generator():

    def __init__(self, size):
        
        self.BOARD_LENGTH = size
        self.grid = [['--' for _ in range(self.BOARD_LENGTH)] for _ in range(self.BOARD_LENGTH)]
        self.grid_solution = copy.deepcopy(self.grid)
        self.PIECES_MAP = copy.deepcopy(self.grid)
        self.black_coordinates = []
        self.white_coordinates = []

        self.LIGHT_RATIO = 0.4
        self.BLACK_ZERO_RATIO = 0.1

    def inside_click(self, x, y):
        return (x in range(0, self.BOARD_LENGTH) and y in range(0, self.BOARD_LENGTH))
    
    def valid_click(self, row, col):

        # This click is not inside the board
        if not self.inside_click(row, col):
            return False

        piece = self.get_cell(row, col).value

        # This cell is black
        if piece[0] == 'b':
            return False
        
        return True
    
    def get_cell(self, row, col):
        return self.PIECES_MAP[row][col]
    
    def set_value(self, row, col, value):
        self.PIECES_MAP[row][col].value = value
        return
    
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
    
    def make_move(self, Move):

        row, col = Move[0], Move[1]
        cell = self.get_cell(row, col)
        possible_hl = self.possible_highlight(Move)

        for pos in possible_hl:
            piece = self.get_cell(pos[0], pos[1])
            if not piece.illuminated:
                piece.set_illuminated(cell)

        return

    def init_random_black(self):
        
        # Random generate black cell from n -> 2n cells
        black_pieces = random.randrange(self.BOARD_LENGTH, 2 * self.BOARD_LENGTH)
        while len(self.black_coordinates) != black_pieces:
            x, y = random.randrange(0, self.BOARD_LENGTH - 1), random.randrange(0, self.BOARD_LENGTH - 1)
            if (x, y) not in self.black_coordinates:
                self.black_coordinates.append((x, y))
        
        # Creating Cell object for each coordinate
        for y in range(self.BOARD_LENGTH):
            for x in range(self.BOARD_LENGTH):
                if (y,x) in self.black_coordinates:
                    self.PIECES_MAP[y][x] = Cell(y, x, "b-")
                else:
                    self.PIECES_MAP[y][x] = Cell(y, x, "--")
                    self.white_coordinates.append((y, x))
                    

        # Add neighbor
        for y in range(self.BOARD_LENGTH):
            for x in range(self.BOARD_LENGTH):

                cell = self.get_cell(y, x)

                up = [y - 1, x]
                down = [y + 1, x]
                left = [y, x - 1]
                right = [y, x + 1]
                directions = [up, down, left, right]

                for pos in directions:
                    row, col = pos[0], pos[1]

                    if self.inside_click(row, col):
                        neighbor = self.get_cell(row, col)
                        cell.add_neighbor(neighbor)
        return
    
    def init_random_light(self):

        # Set light a round each black cell
        for pos in self.black_coordinates:
            y, x = pos[0], pos[1]
            black_cells = self.get_cell(y, x)

            for neigh in black_cells.neighbors:

                if neigh.value == "b-" or neigh.illuminated:
                    continue
                
                # Set light with a ratio
                if random.random() < self.LIGHT_RATIO:
                    self.make_move(neigh.pos)
        
        # Set light for white cell that is a non-illuminated cell
        for pos in self.white_coordinates:

            cell = self.get_cell(pos[0], pos[1])

            # Set light with a ratio
            if not cell.illuminated:
                self.make_move(cell.pos)
            
            # This action to know the solution of the map
            self.grid_solution[pos[0]][pos[1]] = cell.value
        
        return
    
    def set_tag_for_black(self):

        for pos in self.black_coordinates:
            
            cell = self.get_cell(pos[0], pos[1])
            _, count_lights = cell.num_neighbor_lights()

            if count_lights == 0:
                # Set light with a ratio
                if random.random() < self.BLACK_ZERO_RATIO:
                    cell.value = "b0"
            else:
                if random.random() > self.BLACK_ZERO_RATIO:
                    cell.value = 'b' + str(count_lights)

            # Set grid value
            self.grid[pos[0]][pos[1]] = cell.value
            self.grid_solution[pos[0]][pos[1]] = cell.value

        return


    def map_generation(self):

        self.init_random_black()
        self.init_random_light()
        self.set_tag_for_black()

        return copy.deepcopy(self.grid)

    def print_map(self):

        # Generated map
        for row in self.grid:
            print(' '.join(row))

        print("##### SOLVED MAP BY GENERATOR #####")

        #Solved map
        for row in self.grid_solution:
            print(' '.join(row)) 
        
        return

# My_map = map_generator()
# My_map.map_generation()
# My_map.print_map()


