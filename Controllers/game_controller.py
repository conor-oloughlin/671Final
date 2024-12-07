# Controls the game logic and updates the view
import sys
import os
from datetime import datetime
from tkinter import messagebox
from Views.text_board_view import TextBoardView
from Views.board_view import BoardView

from Models.board_model import BoardModel
from Views.board_view import BoardView
from Views.difficulty_view import DifficultyView

class GameController:
    def __init__(self, board, view):
        """
        Initializes the GameController.

        Preconditions:
        - `board` is an instance of BoardModel.
        - `view` is an instance of either BoardView or TextBoardView.

        Postconditions:
        - Initializes game parameters such as `game_over`, `start_time`, and counters.
        - Links the controller to the view.
        - Sets up the game board and initializes the view.
        - Starts the timer for the game.
        """
        self.board = board
        self.view = view
        self.game_over = False
        self.start_time = None
        self.correct_flag_count = 0
        self.flag_count = 0
        self.clicked_count = 0

        self.view.controller = self
        self.board.setup()
        if isinstance(self.view, BoardView):
            self.view.generateUI()
            
        elif isinstance(self.view, TextBoardView):
            self.view.displayBoard()
        self.updateTimer()

    # Takes action when a cell is left clicked on
    def onClick(self, x, y):
        """
        Handles logic when a cell is left-clicked.

        Preconditions:
        - `x` and `y` are valid indices in the board's grid.

        Postconditions:
        - Reveals the cell if it is not already revealed or flagged.
        - Ends the game if a mine or treasure is clicked.
        - Updates the view and checks if the game is won.
        """
        if self.game_over:
            return

        if self.start_time is None:
            self.start_time = datetime.now()

        cell = self.board.grid[x][y]
        if cell.is_revealed or cell.is_flagged:
            return

        if cell.is_mine:
            cell.reveal()
            self.updateView(x, y)
            self.gameOver(False)
            return
        
        if cell.is_treasure:
            cell.reveal()
            self.updateView(x, y)
            self.gameOver(True)
            return

        if cell.adjacent_mines == 0:
            self.board.clearSurroundingTiles(x, y)
        else:
            cell.reveal()
            self.clicked_count += 1

        self.refreshView()

        if self.clicked_count == (self.board.rows * self.board.cols) - self.board.mines:
            self.gameOver(True)

    # Refreshes the view based on type
    def updateView(self, x=None, y=None):
        """
        Updates the view for a specific cell or refreshes the entire view.

        Preconditions:
        - `x` and `y` are valid indices, or both are None.

        Postconditions:
        - Updates the view for the given cell or the entire board.
        """
        if isinstance(self.view, BoardView):
            if x is not None and y is not None:
                self.view.updateCell(x,y)
        elif isinstance(self.view, TextBoardView):
            self.view.refresh()

    # Helper to update game board based off of view type
    def refreshView(self):
        """
        Refreshes the view based on the current state of the game board.

        Preconditions:
        - The view type is either BoardView or TextBoardView.

        Postconditions:
        - Updates the graphical or text-based view to reflect the board's state.
        """
        if isinstance(self.view, BoardView):
            # Update the view for all revealed cells
            for i in range(self.board.rows):
                for j in range(self.board.cols):
                    if self.board.grid[i][j].is_revealed:
                        self.view.updateCell(i, j)
        elif isinstance(self.view, TextBoardView):
            self.view.displayBoard()

    # Takes action when a cell is right clicked on
    def onRightClick(self, x, y):
        """
        Handles logic when a cell is right-clicked.

        Preconditions:
        - `x` and `y` are valid indices in the board's grid.

        Postconditions:
        - Toggles the flagged state of the cell.
        - Updates the game status and the view.
        """
        if self.game_over:
            return

        cell = self.board.grid[x][y]
        if cell.is_revealed:
            return

        cell.toggle_flag()

        if cell.is_flagged:
            self.flag_count += 1
            if cell.is_mine:
                self.correct_flag_count += 1
        else:
            self.flag_count -= 1
            if cell.is_mine:
                self.correct_flag_count -= 1

        self.view.updateCell(x, y)
        self.refreshView()
        if isinstance(self.view, TextBoardView):
            print(f"Mines: {self.board.mines - self.flag_count}, Time: {self.getTimeElapsed()}")
        else:
            self.view.refreshLabel(self.board.mines - self.flag_count, self.getTimeElapsed())

    # Handles game over logic
    def gameOver(self, won):
        """
        Handles the end of the game.

        Preconditions:
        - `won` is a boolean indicating whether the player won or lost.

        Postconditions:
        - Reveals all cells and displays the game over message.
        - Prompts the user to restart or exit the game.
        """
        self.game_over = True

        if hasattr(self, "timer_id"):
            self.view.window.after_cancel(self.timer_id)

        # Reveal all cells
        for x in range(self.board.rows):
            for y in range(self.board.cols):
                cell = self.board.grid[x][y]
                if cell.is_treasure:
                    cell.reveal()
                if cell.is_mine and not cell.is_flagged:
                    cell.reveal()
                if cell.is_flagged and not cell.is_mine:
                    # Mark wrong flags
                    cell.is_wrong_flag = True
                    cell.reveal()

        # Refresh the view after revealing all cells
        self.refreshView()

        # Display game over message
        if isinstance(self.view, TextBoardView):
            self.view.displayBoard()
            print("Congratulations! You Win!" if won else "Game Over! You Lose.")
            replay = input("Play again? (y/n): ").strip().lower()
            if replay == "y":
                self.restart()
            else:
                print("Thanks for playing!")
                exit()
        elif isinstance(self.view, BoardView):
            def showGameOver():
                if self.view.window.winfo_exists():
                    # For graphical view
                    message = "You Win! Play again?" if won else "You Lose! Play again?"
                    if messagebox.askyesno("Game Over", message):
                        self.restart()
                    else:
                        print("Thanks for playing!")
                        self.view.window.destroy()
                        self.view.window.master.destroy()
            self.view.window.after(1000, showGameOver)

    # Restarts the game
    def restart(self):
        """
        Restarts the game with the same parameters.

        Preconditions:
        - None.

        Postconditions:
        - Resets the board and counters.
        - Initializes the view for a new game.
        """
        if hasattr(self, 'timer_id'):
            self.view.window.after_cancel(self.timer_id)

        self.game_over = False
        self.start_time = None
        self.correct_flag_count = 0
        self.flag_count = 0
        self.clicked_count = 0
        self.board.setup()
        if isinstance(self.view, BoardView):
            for widget in self.view.window.winfo_children():
                widget.destroy()
            
            self.view.generateUI()
        elif isinstance(self.view, TextBoardView):
            self.view.displayBoard()
        self.updateTimer()

    def updateTimer(self):
        """
        Updates the game timer and refreshes the view.

        Preconditions:
        - None.

        Postconditions:
        - Updates the timer in the graphical or text-based view.
        """
        if self.game_over:
            return

        elapsed_time = self.getTimeElapsed()

        if isinstance(self.view, BoardView):
            # For graphical view, update the status label and re-schedule the timer
            self.view.refreshLabel(self.board.mines - self.flag_count, elapsed_time)
            self.timer_id = self.view.window.after(1000, self.updateTimer)
        elif isinstance(self.view, TextBoardView):
            # For text-based view, print the elapsed time directly
            print(f"Time: {elapsed_time}")

    def getTimeElapsed(self):
        """
        Calculates the elapsed time since the game started.

        Preconditions:
        - None.

        Postconditions:
        - Returns a string representing the elapsed time in HH:MM:SS format.
        """
        if self.start_time is None:
            return "00:00:00"
        else:
            delta = datetime.now() - self.start_time
            return str(delta).split('.')[0]
