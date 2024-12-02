# Controls the game logic and updates the view
from datetime import datetime
from tkinter import messagebox

class GameController:
    def __init__(self, board, view):
        self.board = board
        self.view = view
        self.game_over = False
        self.start_time = None
        self.correct_flag_count = 0
        self.flag_count = 0
        self.clicked_count = 0

        self.view.controller = self
        self.board.setup()
        self.view.generateUI()

        self.updateTimer()

    # Takes action when a cell is left clicked on
    def onClick(self, x, y):
        if self.game_over:
            return

        if self.start_time is None:
            self.start_time = datetime.now()

        cell = self.board.grid[x][y]
        if cell.is_revealed or cell.is_flagged:
            return

        if cell.is_mine:
            cell.reveal()
            self.view.updateCell(x, y)
            self.gameOver(False)
            return

        if cell.adjacent_mines == 0:
            self.board.clearSurroundingTiles(x, y)
        else:
            cell.reveal()
            self.clicked_count += 1

        # Update the view for all revealed cells
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                if self.board.grid[i][j].is_revealed:
                    self.view.updateCell(i, j)

        if self.clicked_count == (self.board.rows * self.board.cols) - self.board.mines:
            self.gameOver(True)

    # Takes action when a cell is right clicked on
    def onRightClick(self, x, y):
        if self.game_over:
            return

        cell = self.board.grid[x][y]
        if cell.is_revealed:
            return

        cell.toggle_flag()
        self.view.updateCell(x, y)

        if cell.is_flagged:
            self.flag_count += 1
            if cell.is_mine:
                self.correct_flag_count += 1
        else:
            self.flag_count -= 1
            if cell.is_mine:
                self.correct_flag_count -= 1

        self.view.refreshLabel(self.board.mines - self.flag_count, self.getTimeElapsed())

    def gameOver(self, won):
        self.game_over = True
        for x in range(self.board.rows):
            for y in range(self.board.cols):
                cell = self.board.grid[x][y]
                if cell.is_mine and not cell.is_flagged:
                    cell.reveal()
                if cell.is_flagged and not cell.is_mine:
                    # Mark wrong flags
                    cell.is_wrong_flag = True
                self.view.updateCell(x, y)

        message = "You Win! Play again?" if won else "You Lose! Play again?"
        if messagebox.askyesno("Game Over", message):
            self.restart()
        else:
            self.view.window.quit()

    # Restarts the game
    def restart(self):
        self.game_over = False
        self.start_time = None
        self.correct_flag_count = 0
        self.flag_count = 0
        self.clicked_count = 0
        self.board.setup()
        # self.view.resetUI()
        self.view.generateUI()
        self.updateTimer()

    def updateTimer(self):
        if self.game_over:
            return
        elapsed_time = self.getTimeElapsed()
        self.view.refreshLabel(self.board.mines - self.flag_count, elapsed_time)
        self.view.window.after(1000, self.updateTimer)

    def getTimeElapsed(self):
        if self.start_time is None:
            return "00:00:00"
        else:
            delta = datetime.now() - self.start_time
            return str(delta).split('.')[0]