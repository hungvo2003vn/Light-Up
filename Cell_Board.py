from SETTING import *

#################### CLASS CELL ####################
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
        return ( (self.pos[0] == des[0]) and (self.pos[1] == des[1]) )
    
    # Only for White Cell
    def set_illuminated(self, cell):

        self.illuminated = True
        self.source_illuminated += [cell]

        
        # If current cell is a bulb
        if self.is_bulb:
            if self.is_overlap():
                self.value = "fw"
        else:

            # This is the case setting a light up
            if self.same_pos(cell.pos):
                self.is_bulb = True

                if self.is_overlap():
                    self.value = "fw"
                else:
                    self.value = "fr"
            # Not a light and illuminated by cell
            else:
                self.value = 'f' +  self.value[1]
        
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
            self.illuminated = False
            self.value = '-' +  self.value[1]

        # Toggle itself
        if self.same_pos(cell.pos) and self.is_bulb:
            self.is_bulb = False
            self.value = self.value[0] + '-'
        
        # If this self's cell is a bulb and not overlap
        elif self.is_bulb and not self.is_overlap():
                self.value = "fr"

        return len(self.source_illuminated) == 0