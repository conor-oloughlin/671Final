from Models.board_model import BoardModel
from Controllers.game_controller import GameController
from Views.board_view import BoardView
from Views.difficulty_view import DifficultyView
from Views.text_board_view import TextBoardView

if __name__=="__main__":
    difficulty = DifficultyView()
    if difficulty.level == "beginner":
        rows = 8
        cols = 8
        mines = 10
        treasures = 1
    elif difficulty.level == "intermediate":
        rows = 16
        cols = 16
        mines = 40
        treasures = 3
    elif difficulty.level == "expert":
        rows = 30
        cols = 16
        mines = 99
        treasures = 5
    else:
        rows = 8
        cols = 8
        mines = 10
        treasures = 1
    
    board = BoardModel(rows, cols, mines)
    # view = BoardView(board)  # Graphical view
    view = TextBoardView(board)  # Text-based view
    controller = GameController(board, view)
    view.controller = controller

    if isinstance(view, TextBoardView):
        while not controller.game_over:
            view.promptMove()
    else: 
        view.window.mainloop()