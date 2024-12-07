# Controls the testing logic
import sys
import os
import csv
from datetime import datetime
from tkinter import messagebox, filedialog
from Views.text_board_view import TextBoardView
from Views.board_view import BoardView

from Models.board_model import BoardModel
from Views.board_view import BoardView
from Models.cell_model import Cell

class TestController: 
    def __init__(self, file_path):
        """
        Initializes the TestController with a given file path.

        Preconditions:
        - `file_path` is a valid path to a CSV file containing the board configuration.

        Postconditions:
        - `self.game_board` is initialized as a `BoardModel` in testing mode.
        - `self.file_contents` contains the board data read from the file.
        - `self.is_valid` is set to True if the board is valid, otherwise False.
        """
        self.file_path = file_path
        self.game_board = BoardModel(is_testing=True)
        self.file_contents = self.read_board(self.file_path)
        self.is_valid = self.validate_board(self.file_contents)


    def read_board(self, file_path):
        """
        Reads the board configuration from the specified CSV file.

        Preconditions:
        - `file_path` is a valid path to a CSV file.

        Postconditions:
        - `self.game_board.rows` and `self.game_board.cols` are set based on the file's dimensions.
        - `self.game_board.grid` is populated with `Cell` instances based on the file's content.
        - Returns the board data as a list of lists.
        """
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            tmp = [[int(cell) for cell in row] for row in reader]

            # Set rows and cols based on the CSV
            self.game_board.rows = len(tmp)
            self.game_board.cols = len(tmp[0])

            # Assign the data to the board's grid
            self.game_board.grid = [
                [Cell(is_mine=(cell == 1), is_treasure=(cell == 2)) for cell in row] for row in tmp
            ]
        return tmp

    def validate_board(self, board):
        """
        Validates the board configuration.

        Preconditions:
        - `board` is a list of lists representing the board.

        Postconditions:
        - Returns True if the board is valid, otherwise False.
        - Prints error messages for invalid board properties.
        """
        # Check board size
        if len(board) != 8 or any(len(row) != 8 for row in board):
            print("Invalid board size")
            return False

        valid_values={0,1,2}
        if any(num not in valid_values for row in self.file_contents for num in row):
            for row in board:
                for cell in row:
                    if cell not in valid_values:
                        print(f"Invalid cell value: {cell}")
            return False
        self.game_board.mine_positions = [(r, c) for r, row in enumerate(self.file_contents) for c, cell in enumerate(row) if cell == 1]
        self.game_board.treasure_positions = [(r, c) for r, row in enumerate(self.file_contents) for c, cell in enumerate(row) if cell == 2]
        self.game_board.mines = len(self.game_board.mine_positions)
        self.game_board.treasures = len(self.game_board.treasure_positions)

        # Validate mine locations and treasures
        if self.game_board.mines > 10:
            print("Invalid number of mines")
            return False
        if not self.validate_mines(self.game_board.mine_positions):
            print("Invalid mine locations")
            return False

        if self.game_board.treasures > 9: 
            print("Invalid number of treasures")
            return False


        return True

    # Validates mine locations with relaxed constraints. These constraints were relaxed as it was not possible to generate a valid board with the original constraints.
    def validate_mines(self, mines):
        """
        Validates the placement of mines with specific constraints.

        Preconditions:
        - `mines` is a list of (row, column) tuples representing mine positions.

        Postconditions:
        - Returns True if the mine placement is valid, otherwise False.
        """
        # ensures one of the first 8 mines is on a cell where the row and column are equal
        has_diagonal = False
        for mine in mines:
            if mine[0] == mine[1]:
                has_diagonal = True
                break
    
        if not has_diagonal:
            return False
        
        # ensures the one of the mines is adjacent to another
        has_adjacent = False
        for i in range(len(mines)):
            for j in range(i+1, len(mines)):
                row1, col1 = mines[i]
                row2, col2 = mines[j]
                if abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1:
                    has_adjacent = True
                    break
            
        if not has_adjacent:
            return False

        # ensures a mine is not adjacent to another
        has_not_adjacent = False
        for i in range(len(mines)):
            if has_not_adjacent:
                break
            row1, col1 = mines[i]
            for j in range(len(mines)):
                if i == j:
                    continue
                row2, col2 = mines[j]
                if abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1:
                    continue
                else:
                    has_not_adjacent = True
                    break
        
        if not has_not_adjacent:
            return False
        
        return True