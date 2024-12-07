from Models.board_model import BoardModel
from Controllers.game_controller import GameController
from Views.board_view import BoardView
from Views.difficulty_view import DifficultyView
from Views.text_board_view import TextBoardView
from Views.testing_view import TestingView
from Views.mode_view import ModeView
from Controllers.test_controller import TestController
import tkinter as tk

if __name__=="__main__":
    # Creates the root window and hides it
    root = tk.Tk("root")
    root.withdraw()

    # Creates mode view and closes it after the user selects a mode
    mode_view = ModeView(root)
    root.wait_window(mode_view.window)

    # Creates testing view
    testing_view = TestingView(root)

    if testing_view.is_testing:
        # Prompts the user for a file and validates it if they select testing mode
        file_path = testing_view.uploadCSV(root)
        if not file_path:
            print("No valid test board selected. Exiting the game.")
            exit()
        test_controller = TestController(file_path)
        if not test_controller.is_valid:
            print("Invalid test board. Exiting the game.")
            exit()
        board = test_controller.game_board
    else:
        # Creates a board according to the user's desired difficulty if they don't select testing mode
        difficulty_view = DifficultyView(root)
        root.wait_window(difficulty_view.window)
        rows = difficulty_view.rows
        cols = difficulty_view.cols
        mines = difficulty_view.mines
        treasures = difficulty_view.treasures
        board = BoardModel(rows, cols, mines, treasures)

    # Creates the game board and view based on the user's selected mode
    if mode_view.mode == "graphical":
        view = BoardView(board, root)
        controller = GameController(board, view)
        root.mainloop()
        root.wait_window(view.window)
        root.destroy()
    elif mode_view.mode == "text":
        view = TextBoardView(board)
        controller = GameController(board, view)
        while not controller.game_over:
            view.promptMove()
    else:
        print("No mode selected. Exiting the game.")