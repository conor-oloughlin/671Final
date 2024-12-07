import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import *
from Models.board_model import BoardModel

class BoardView:
    def __init__(self, board, root, controller=None):
        # Defines controller and game board
        self.controller = controller
        self.board = board

        self.window = tk.Toplevel(root)
        self.window.title("Minesweeper")
        self.frame = None

        self.tiles = {}
        self.status_label = None
    
    # Builds the graphical UI for the game
    def generateUI(self):
        if hasattr(self, "frame") and self.frame is not None and self.frame.winfo_exists():
            self.frame.destroy()
        
        self.frame = tk.Frame(self.window)
        self.frame.pack()

        self.images = {
            "plain": PhotoImage(file = "images/tile_plain.gif"),
            "clicked": PhotoImage(file = "images/tile_clicked.gif"),
            "mine": PhotoImage(file = "images/tile_mine.gif"),
            "treasure": PhotoImage(file = "images/tile_treasure.gif"),
            "flag": PhotoImage(file = "images/tile_flag.gif"),
            "wrong": PhotoImage(file = "images/tile_wrong.gif"),
            "numbers": [PhotoImage(file = f"images/tile_{i}.gif") for i in range(1, 9)]
        }
     
        # Generates tiles for the game board
        for x in range(self.board.rows):
            self.tiles[x] = {}
            for y in range(self.board.cols):
                button = tk.Button(self.frame, image = self.images["plain"], width=20, height=20)
                button.grid(row=x + 1, column=y)

                button.bind("<Button-1>", self.onClickWrapper(x, y))
                button.bind("<Button-3>", self.onRightClickWrapper(x, y))

                self.tiles[x][y] = button
        
        self.status_label = tk.Label(self.frame, text="Mines: {self.board.mines} Time: 0")
        self.status_label.grid(row=self.board.rows + 1, column=0, columnspan=self.board.cols)

    # Updates cells according to their state
    def updateCell(self, x, y):
        if not self.window.winfo_exists():
            return

        cell = self.board.grid[x][y]
        button = self.tiles[x][y]

        if cell.is_revealed:
            if cell.is_mine:
                button.config(image=self.images["mine"])
            elif cell.is_treasure:
                button.config(image=self.images["treasure"])
            elif cell.adjacent_mines > 0:
                button.config(image=self.images["numbers"][cell.adjacent_mines - 1])
            else:
                button.config(image=self.images["clicked"])
        elif cell.is_flagged:
            button.config(image=self.images["flag"])
        else:
            button.config(image=self.images["plain"])
    
    # Updates elements of the game status including the remaining mines and time elapsed
    def refreshLabel(self, remaining_mines, time_elapsed):
        if self.window.winfo_exists() and self.status_label.winfo_exists():
            self.status_label.config(text=f"Mines: {remaining_mines} Time: {time_elapsed}")
    
    # Wrapper for the onClick function that handles left clicks
    def onClickWrapper(self, x, y):
        return lambda event: self.controller.onClick(x, y)
        
    
    # Wrapper for the onRightClick function that handles right clicks
    def onRightClickWrapper(self, x, y):
        return lambda event: self.controller.onRightClick(x, y)

