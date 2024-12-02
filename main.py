from Models.board_model import BoardModel
from Controllers.game_controller import GameController
from Views.board_view import BoardView

if __name__=="__main__":
    rows = 10
    cols = 10
    mines = 10

    board = BoardModel(rows, cols, mines)
    view = BoardView(board)
    controller = GameController(board, view)
    view.controller = controller
    view.window.mainloop()