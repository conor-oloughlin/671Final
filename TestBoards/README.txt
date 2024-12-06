
Minesweeper CSV Test Files

This folder contains valid and invalid test boards to test the functionality of loading Minesweeper boards from CSV files. Each file is described below, along with the expected behavior when the game processes the file.

------------------------------------------------------------------------
Test Files and Expected Behavior

File Name              | Description                                                               | Expected Behavior
-----------------------|---------------------------------------------------------------------------|------------------------------------------------------------------
valid_board_1.csv      | A standard 8x8 Minesweeper board with 10 mines and no treasures.         | The game should load successfully, place 10 mines, and calculate adjacent mine counts correctly.
valid_board_2.csv      | An 8x8 board with 10 mines and treasures placed at a few locations.      | The game should load successfully, place 10 mines, treasures, and calculate adjacent counts.
invalid_board_1.csv    | A 7x8 board (incorrect dimensions: one row missing).                    | The game should raise an error: "Invalid board size in CSV file."
invalid_board_2.csv    | An 8x9 board (extra column in one row).                                 | The game should raise an error: "Invalid board size in CSV file."
invalid_board_3.csv    | An 8x8 board with 12 mines (too many mines).                            | The game should raise an error: "Too many mines in the CSV file."
invalid_board_4.csv    | An 8x8 board with invalid cell values (3 and -1).                       | The game should raise an error: "Invalid cell value in CSV file."
invalid_board_5.csv    | An 8x8 board with non-numeric values (X and Mine).                      | The game should raise an error: "Invalid cell value in CSV file."

------------------------------------------------------------------------
File Format

Each CSV file must adhere to the following conventions for valid boards:
- Dimensions: The board must be 8 rows by 8 columns.
- Cell Values:
  - 0: Empty cell
  - 1: Mine
  - 2: Treasure (optional, depending on game mode)
- The board must contain exactly 10 mines (1 values).
- All cells must contain numeric values (0, 1, or 2).

------------------------------------------------------------------------
How to Use

1. Run the Game:
   - Run the game and specify the path to a test file when prompted (or modify the main script to load a specific file automatically).

2. Expected Behavior:
   - For valid boards, the game should load the board and display the Minesweeper grid.
   - For invalid boards, the game should display an error message and prevent the game from starting.

3. Debugging:
   - Use the error messages to verify the program’s ability to detect and handle invalid input files.

------------------------------------------------------------------------
