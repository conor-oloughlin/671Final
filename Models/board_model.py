# Model for the game board
from collections import deque
import random
from Models.cell_model import Cell

class BoardModel:
    # Sets the initial board parameters
    def __init__(self, rows=8, cols=8, mines=10, treasures=1, mine_positions=None, treasure_positions=None, is_testing=False):
        """
        Initializes the BoardModel with the specified parameters.

        Preconditions:
        - `rows` and `cols` are positive integers representing the board dimensions.
        - `mines` and `treasures` are non-negative integers.
        - If provided, `mine_positions` and `treasure_positions` are lists of valid cell coordinates.

        Postconditions:
        - `self.rows`, `self.cols`, `self.mines`, and `self.treasures` are set.
        - `self.grid` is initialized as a 2D list of `Cell` instances.
        - `self.mine_positions` and `self.treasure_positions` are set or initialized as empty lists.
        - `self.is_testing` determines whether the board is in testing mode.
        """
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.treasures = treasures
        self.mine_positions = mine_positions if mine_positions is not None else []
        self.treasure_positions = treasure_positions if treasure_positions is not None else []
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.is_testing = is_testing
    
    # Sets up the initial board state. A reengineered version of the setup function.
    def setup(self):
        """
        Sets up the initial board state with mines, treasures, and adjacent mine counts.

        Preconditions:
        - `self.rows` and `self.cols` define the board dimensions.
        - `self.mines` and `self.treasures` are non-negative integers.

        Postconditions:
        - Mines and treasures are randomly placed unless `is_testing` is True.
        - Adjacent mine counts are calculated for each cell.
        - The board is ready for gameplay.
        """
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None
        self.grid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

        if not self.is_testing:
            # Creates the mine positions if positions aren't know
            self.mine_positions = random.sample(
                [(x, y) for x in range(self.rows) for y in range(self.cols)], self.mines
            )
            

            # Creates the treasure positions if positions aren't know
            self.treasure_positions = random.sample(
                [(x, y) for x in range(self.rows) for y in range(self.cols) if (x, y) not in self.mine_positions], self.treasures
            )
            
        # Sets is_mine property to true for each mine position
        for x, y in self.mine_positions:
            self.grid[x][y].is_mine = True
        for x, y in self.treasure_positions:
            self.grid[x][y].is_treasure = True
        
        # Determines adjacent mines for each cell
        for x in range(self.rows):
            for y in range(self.cols):
                neighbors = self.getNeighbors(x, y)
                num_mines = sum(1 for nX, nY in neighbors if self.grid[nX][nY].is_mine)
                self.grid[x][y].adjacent_mines = num_mines

    # Gets all neighboring cells of the provided cell
    def getNeighbors(self, x, y):
        """
        Gets all valid neighboring cells for the cell at (x, y).

        Preconditions:
        - `x` and `y` are valid indices within the grid.

        Postconditions:
        - Returns a list of (x, y) tuples representing valid neighbor coordinates.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbor_cells = []

        for dirX, dirY in directions:
            nextX, nextY = x + dirX, y + dirY

            if 0 <= nextX < self.rows and 0 <= nextY < self.cols:
                neighbor_cells.append((nextX, nextY))
        return neighbor_cells
    
    # Clears all cells surronding the given coordinates that match necessary conditions
    def clearSurroundingTiles(self, x, y):
        """
        Clears all cells around (x, y) that meet necessary conditions.

        Preconditions:
        - `x` and `y` are valid indices within the grid.

        Postconditions:
        - Reveals cells recursively if they have no adjacent mines.
        - Stops clearing at cells with adjacent mines or flagged cells.
        """
        queue = deque([(x, y)])

        while queue:
            currX, currY = queue.popleft()
            for neighborX, neighborY in self.getNeighbors(currX, currY):
                if neighborX < 0 or neighborX >= self.rows or neighborY < 0 or neighborY >= self.cols:
                    continue
                
                cell = self.grid[neighborX][neighborY]
                
                if not cell.is_revealed and not cell.is_flagged:
                    self.clearTile(neighborX, neighborY, queue)
    
    # Determines if a cell should be cleared and revealed.
    def clearTile(self, x, y, queue):
        """
        Clears and reveals a specific tile at (x, y).

        Preconditions:
        - `x` and `y` are valid indices within the grid.
        - `queue` is a deque used for recursive clearing.

        Postconditions:
        - The tile is revealed if it is not a mine or treasure.
        - If the tile has no adjacent mines, it is added to the queue for further clearing.
        """
        cell = self.grid[x][y]

        if cell.is_revealed or cell.is_flagged:
            return
        
        if cell.adjacent_mines == 0 and not cell.is_mine and not cell.is_treasure:
            cell.reveal()
            queue.append((x, y))
        elif cell.adjacent_mines > 0 and not cell.is_mine and not cell.is_treasure:
            cell.reveal()