import random
import copy

class map_generator:

    def __init__(self, n, black_cell_options):

        self.n = n
        self.black_cell_options = copy.deepcopy(black_cell_options)

        self.grid = [['--' for _ in range(self.n)] for _ in range(self.n)]
        self.black_cell_count = random.randint(n, 2 * n)
        self.RANDOM_RATIO = 0.3

    def inside(self, row, col):
        return (row in range(self.n) and col in range(self.n))
    
    def directions(self, row, col):
        up = [row - 1, col]
        down = [row + 1, col]
        left = [row, col - 1]
        right = [row, col + 1]
        
        ans = []
        result = [up, left, down, right]
        for pos in result:
            if self.inside(pos[0], pos[1]):
                ans.append(pos)
            
        return ans
    
    def white_need(self, row, col):
    
        if self.grid[row][col] == 'b-' or self.grid[row][col] == '--':
            return -1
            
        need = self.grid[row][col][1]
        return int(need)
    
    def is_valid_cell(self, row, col):

        need = self.white_need(row, col)
        if need == -1:
            return True
        
        count_white = 0
        directs = self.directions(row, col)
        for pos in directs:
            r, c = pos[0], pos[1]
            if self.grid[r][c] == "--":
                count_white += 1
                
        return need == count_white
    
    def is_valid_placement(self, row, col):
    
        if not self.is_valid_cell(row, col):
            return False
            
        directs = self.directions(row, col)
        for pos in directs:
            r, c = pos[0], pos[1]
            if not self.is_valid_cell(r, c):
                return False
        
        return True
    
    def find_valid(self, row, col):
    
        # Maybe a black
        if self.black_cell_count and random.random() < self.RANDOM_RATIO:
            
            choices = copy.deepcopy(self.black_cell_options)
            while len(choices) > 0:
                
                value = random.choice(choices)
                choices.remove(value)
                self.grid[row][col] = value
                
                if self.is_valid_placement(row, col):
                    return (self.black_cell_count - 1)
                
        value = "--"
        self.grid[row][col] = value
        
        return self.black_cell_count
    
    def generate_map(self):
        
        for row in range(self.n):
            for col in range(self.n):
                self.black_cell_count = self.find_valid(row, col)
                #if grid[row][col][0] == 'b':
                    #print(grid[row][col], white_need(grid, row, col),[row,col] ,is_valid_placement(grid, row, col))
        
        return self.grid

    def print_map(self):

        for row in self.grid:
            print(' '.join(row))
        
        # Check map
        new_grid = [['--' for _ in range(self.n)] for _ in range(self.n)]
        for row in range(self.n):
            for col in range(self.n):
                
                if self.grid[row][col][0] != 'b':
                    continue
                if self.is_valid_placement(row, col):
                    new_grid[row][col] = 'T-'
                else:
                    new_grid[row][col] = 'F-'
        
        print("###### CHECK MAP ######")    
        for row in new_grid:
            print(' '.join(row))
        
        return

# # Example usage
# MY_MAP = map_generator(7, ["b-", "b0", "b1", "b2", "b3", "b4"])
# MY_MAP.generate_map()
# MY_MAP.print_map()

