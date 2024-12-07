# Model for the game board
from collections import deque
import random
from Models.cell_model import Cell

class BoardModel:
    # Sets the initial board parameters
    def __init__(self, rows=8, cols=8, mines=10, treasures=1, mine_positions=None, treasure_positions=None):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.treasures = treasures
        self.mine_positions = mine_positions if mine_positions is not None else []
        self.treasure_positions = treasure_positions if treasure_positions is not None else []
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
    
    # Sets up the initial board state. A reengineered version of the setup function.
    def setup(self):
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None
        self.grid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

        if not any(cell.is_mine for row in self.grid for cell in row):
            if not self.mine_positions:
                # Creates the mine positions if positions aren't know
                self.mine_positions = random.sample(
                    [(x, y) for x in range(self.rows) for y in range(self.cols)], self.mines
                )
            # Sets is_mine property to true for each mine position
            for x, y in self.mine_positions:
                self.grid[x][y].is_mine = True

            if not self.treasure_positions:
                # Creates the treasure positions if positions aren't know
                self.treasure_positions = random.sample(
                    [(x, y) for x in range(self.rows) for y in range(self.cols) if (x, y) not in self.mine_positions], self.treasures
                )
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
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbor_cells = []

        for dirX, dirY in directions:
            nextX, nextY = x + dirX, y + dirY

            if 0 <= nextX < self.rows and 0 <= nextY < self.cols:
                neighbor_cells.append((nextX, nextY))
        return neighbor_cells
    
    # Clears all cells surronding the given coordinates that match necessary conditions
    def clearSurroundingTiles(self, x, y):
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
        cell = self.grid[x][y]

        if cell.is_revealed or cell.is_flagged:
            return
        
        if cell.adjacent_mines == 0 and not cell.is_mine and not cell.is_treasure:
            cell.reveal()
            queue.append((x, y))
        elif cell.adjacent_mines > 0 and not cell.is_mine and not cell.is_treasure:
            cell.reveal()