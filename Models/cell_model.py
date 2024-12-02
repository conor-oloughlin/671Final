# New class to represent a cell in the minesweeper game

class Cell:
    # Initializes a cell with necessary parameters
    def __init__(self, is_mine=False, is_flagged=False, is_revealed=False, adj_mines=0, is_treasure=False):
        self.is_mine = is_mine
        self.is_flagged = is_flagged
        self.is_revealed = is_revealed
        self.adjacent_mines = adj_mines
        self.is_treasure = is_treasure
    
    # Returns true if a cell is a mine when it is revealed and false otherwise.
    def reveal(self):
        if not self.is_flagged:
            self.is_revealed = True
            return self.is_mine
        return None
    
    # Toggles the flag parameters of a cell.
    def toggle_flag(self):
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged