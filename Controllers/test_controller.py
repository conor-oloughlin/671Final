# Controls the game logic and updates the view
import sys
import os
import csv
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from tkinter import messagebox, filedialog
from Views.text_board_view import TextBoardView
from Views.board_view import BoardView

from Models.board_model import BoardModel
from Views.board_view import BoardView
from Models.cell_model import Cell

class TestController: 
    def __init__(self, file_path):
        self.file_path = file_path
        self.game_board = BoardModel()
        self.file_contents = self.read_board(self.file_path)
        if self.game_board:
            self.validate_board(self.game_board.grid)


    def read_board(self, file_path):
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
        # Check board size
        if len(board) != 8 or any(len(row) != 8 for row in board):
            return False

        valid_values={0,1,2}
        if any(cell not in valid_values for row in board for cell in row):
            return False

        self.game_board.mines_positions = [(r, c) for r, row in enumerate(board) for c, cell in enumerate(row) if cell == 1]
        self.game_board.treasures_positions = [(r, c) for r, row in enumerate(board) for c, cell in enumerate(row) if cell == 2]
        self.game_board.mines = len(self.game_board.mines_positions)
        self.game_board.treasures = len(self.game_board.treasures_positions)

        # Validate mine locations and treasures
        if len(self.game_board.mines) != 10:
            return False
        if not self.validate_mines(self.game_board.mines):
            return False

        if len(self.game_board.treasures) > 9: 
            return False

        return True

    def validate_mines(self, mines):
        # Check that first 8 mines are in unique rows & cols
        first_eight = mines[:8]
        if len({r for r, _ in first_eight}) != 8 or len({c for _, c in first_eight}) != 8:
            return False
        if any(abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1 for (r1, c1) 
                in first_eight for (r2, c2) in first_eight if (r1, c1) != (r2, c2)):
            return False

        # Check remaining mines
        ninth = mines[8]
        if not any(abs(ninth[0] - r) + abs(ninth[1] - c) == 1 for r, c in first_eight):
            return False
        tenth = mines[9]
        if any(abs(tenth[0] - r) <= 1 and abs(tenth[1] - c) <= 1 for r, c in mines[:9]):
            return False
        return True