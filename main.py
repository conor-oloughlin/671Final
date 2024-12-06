from Models.board_model import BoardModel
from Controllers.game_controller import GameController
from Views.board_view import BoardView
from Views.difficulty_view import DifficultyView
from Views.text_board_view import TextBoardView
from Views.testing_view import TestingView
from Controllers.test_controller import TestController

# def wait_for_file_path():
#     if not(is_waiting):
#         is_waiting = True
#         time.sleep(0.1)
#         is_waiting = False
#     if testing.file_path is not None:
#         return True
#     else:
#         wait_for_file_path()

if __name__=="__main__":
    is_waiting = False
    testing = TestingView()
    if testing.is_testing:
        file_path = testing.uploadCSV()
        test_controller = TestController(file_path)

    else:
        difficulty = DifficultyView()
        rows = difficulty.rows
        cols = difficulty.cols
        mines = difficulty.mines
        treasures = difficulty.treasures
    
    if testing.is_testing:
        board = test_controller.game_board
    else:
        board = BoardModel(rows, cols, mines)
    view = BoardView(board)  # Graphical view
    # view = TextBoardView(board)  # Text-based view
    controller = GameController(board, view)
    view.controller = controller

    if isinstance(view, TextBoardView):
        while not controller.game_over:
            view.promptMove()
    else: 
        view.window.mainloop()

