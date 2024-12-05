class TextBoardView:
    def __init__(self, board, controller=None):
        self.board = board
        self.controller = controller

    def displayBoard(self):
        print("\nCurrent Board:")
        print("   " + " ".join([f"{col}" for col in range(self.board.cols)]))
        print("  +" + "---" * self.board.cols + "+")

        for x in range(self.board.rows):
            row = [self._cellDisplay(self.board.grid[x][y]) for y in range(self.board.cols)]
            print(f"{x:2}|" + " ".join(row) + "|")

        print("  +" + "---" * self.board.cols + "+")

    def _cellDisplay(self, cell):
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
        move = input("Enter your move (e.g., 'R 1 2' for reveal or 'F 1 2' for flag): ").strip().split()
        if len(move) == 3:
            action, x, y = move[0].upper(), move[1], move[2]
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
        self.displayBoard()