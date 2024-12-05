from Models.board_model import BoardModel
from Controllers.game_controller import GameController
from Views.board_view import BoardView
from Views.text_board_view import TextBoardView

if __name__=="__main__":
    rows = 10
    cols = 10
    mines = 10

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