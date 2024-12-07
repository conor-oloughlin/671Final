# New class to represent a cell in the minesweeper game

class Cell:
    # Initializes a cell with necessary parameters
    def __init__(self, is_mine=False, is_flagged=False, is_revealed=False, adj_mines=0, is_treasure=False):
        """
        Initializes a Cell with the given attributes.

        Preconditions:
        - `is_mine`, `is_flagged`, `is_revealed`, and `is_treasure` are boolean values.
        - `adj_mines` is a non-negative integer representing the number of adjacent mines.

        Postconditions:
        - `self.is_mine`, `self.is_flagged`, `self.is_revealed`, `self.adjacent_mines`, and `self.is_treasure` are initialized.
        """
        self.is_mine = is_mine
        self.is_flagged = is_flagged
        self.is_revealed = is_revealed
        self.adjacent_mines = adj_mines
        self.is_treasure = is_treasure
    
    # Returns true if a cell is a mine when it is revealed and false otherwise.
    def reveal(self):
        """
        Reveals the cell if it is not flagged.

        Preconditions:
        - `self.is_flagged` is False.

        Postconditions:
        - `self.is_revealed` is set to True if the cell is not flagged.
        """
        if not self.is_flagged:
            self.is_revealed = True
    
    # Toggles the flag parameters of a cell.
    def toggle_flag(self):
        """
        Toggles the flagged state of the cell.

        Preconditions:
        - `self.is_revealed` is False.

        Postconditions:
        - `self.is_flagged` is toggled between True and False.
        """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged