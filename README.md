671 Final Project: Reengineered Minesweeper
===========================

# Instructions:
----------------
- To play the minesweeper game, run the main.py function.

# Reengineering Documentation:
-----------------------------
- See the Reengineering Function Table pdf located in this repository for information on the conversion of this program from a single file script to a Model-View-Controller Application.
- A markdown version of this table can be found below:
# 671 Final Project Documentation

| Original Function MVC Component | Reengineered Class/Function       | Notes                                                                                  |
|---------------------------------|-----------------------------------|----------------------------------------------------------------------------------------|
| `__init__` Controller           | `GameController.__init__()`       | Initializes a new game state with an accompanying board and view.                      |
| `setup()` Model                 | `BoardModel.setup()`              | Creates the initial board state, including generating mine positions and calculating adjacent mines for each cell. |
| `restart()` Controller          | -                                 |                                                                                        |
| `refreshLabels()` View          | `BoardView.refreshLabel()`        | Refreshes the status label to ensure the remaining mines and time are accurately displayed. |
| `gameOver()` Controller         | `GameController.gameOver()`       | Handles logic relating to the ending of the game.                                      |
| `updateTimer` Controller        | `GameController.updateTimer()`    | Updates the timer.                                                                     |
| `getNeighbors()` Model          | `BoardModel.getNeighbors()`       | Returns a list of all cells that are neighbors of the cell at the given `(x, y)` location. |
| `onClickWrapper()` View         | `BoardView.onClickWrapper()`      | Wrapper to handle left-click events.                                                  |
| `onRightClickWrapper()` View    | `BoardView.onRightClickWrapper()` | Wrapper to handle right-click events.                                                 |
| `onClick()` Controller          | -                                 |                                                                                        |
| `onRightClick()` Controller     | -                                 |                                                                                        |
| `clearSurroundingTiles()` Model | `BoardModel.clearSurroundingTiles()` | Moves outward using BFS to determine which cells should be revealed when a given cell is clicked. |
| `clearTiles()` Model            | `BoardModel.clearTile()`          | Determines if a specific cell should be revealed when clearing surrounding cells.      |
| `main.py` Entry Point           | N/A                               | The `main.py` file acts as the driver for this application. When the user wants to play the game, they should run the `main.py` file. |
