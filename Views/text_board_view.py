class TextBoardView:
    """
    Represents a text-based view for a Minesweeper game.
    """
    def __init__(self, board, controller=None):
        """
        Initializes the TextBoardView.

        Preconditions:
        - `board` is an instance of BoardModel.
        - `controller` is either None or an instance of GameController.

        Postconditions:
        - `self.board` is set to the provided `board`.
        - `self.controller` is set to the provided `controller`.
        """
        self.board = board
        self.controller = controller

    def displayBoard(self):
        """
        Displays the current state of the board in a text-based format.

        Preconditions:
        - `self.board` contains a valid grid with `rows` and `cols` attributes.
        - Each cell in `self.board.grid` has `is_revealed`, `is_mine`, `is_flagged`, and `adjacent_mines` attributes.

        Postconditions:
        - Outputs the current board state to the console.
        """
        print("\nCurrent Board:")
        print("   " + " ".join([f"{col}" for col in range(self.board.cols)]))
        print("  +" + "---" * self.board.cols + "+")

        for x in range(self.board.rows):
            row = [self._cellDisplay(self.board.grid[x][y]) for y in range(self.board.cols)]
            print(f"{x:2}|" + " ".join(row) + "|")

        print("  +" + "---" * self.board.cols + "+")

    def _cellDisplay(self, cell):
        """
        Returns a character representing the display state of a single cell.

        Preconditions:
        - `cell` is an instance of a cell object with attributes `is_revealed`, `is_mine`, `is_flagged`, and `adjacent_mines`.

        Postconditions:
        - Returns "M" if the cell is a revealed mine.
        - Returns the number of adjacent mines if the cell is revealed and has adjacent mines.
        - Returns " " (space) if the cell is revealed and has no adjacent mines.
        - Returns "F" if the cell is flagged.
        - Returns "#" if the cell is not revealed and not flagged.
        """
        if cell.is_revealed:
            if cell.is_mine:
                return "M"
            elif cell.adjacent_mines > 0:
                return str(cell.adjacent_mines)
            else:
                return " "
        elif cell.is_flagged:
            return "F"
        else:
            return "#"

    def promptMove(self):
        """
        Prompts the user to enter a move, processes it, and forwards it to the controller.

        Preconditions:
        - The user input follows the format "R x y" (reveal) or "F x y" (flag) or "exit".

        Postconditions:
        - Calls `self.controller.onClick(x, y)` if the user enters "R x y".
        - Calls `self.controller.onRightClick(x, y)` if the user enters "F x y".
        - Exits the game if the user enters "exit".
        - Prints an error message if the input format is invalid.
        """
        move = input("Enter your move (e.g., 'R 1 2' for reveal or 'F 1 2' for flag): ").strip()
        if move == "exit":
            print("Thanks for playing! Exiting the game...")
            exit()
        parts = move.split()
        if len(parts) == 3:
            action, x, y = parts[0].upper(), parts[1], parts[2]
            try:
                x, y = int(x), int(y)
                if action == "R":
                    self.controller.onClick(x, y)
                elif action == "F":
                    self.controller.onRightClick(x, y)
                else:
                    print("Invalid action. Use 'R' to reveal or 'F' to flag.")
            except ValueError:
                print("Invalid input. Please enter numeric coordinates.")
        else:
            print("Invalid input format. Use 'R x y' or 'F x y'.")

    def gameOver(self, won):
        """
        Handles the game over scenario.

        Preconditions:
        - `won` is a boolean indicating whether the player has won (True) or lost (False).

        Postconditions:
        - Displays the final board state using `self.displayBoard()`.
        - Prompts the user to replay or exit.
        - If the user chooses to replay, calls `self.controller.restart()`.
        - Exits the game if the user chooses not to replay.
        """
        self.displayBoard()
        if won:
            print("Congratulations! You Win!")
        else:
            print("Game Over! You Lose.")
        replay = input("Play again? (y/n): ").strip().lower()
        if replay == "y":
            self.controller.restart()
        else:
            print("Thanks for playing!")
            exit()

    def refresh(self):
        """
        Refreshes the board display.

        Preconditions:
        - `self.board` contains an up-to-date grid state.

        Postconditions:
        - Calls `self.displayBoard()` to redraw the board in its current state.
        """
        self.displayBoard()