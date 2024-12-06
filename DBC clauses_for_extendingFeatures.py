# Python Version 2.7.3
# File: minesweeper.py

from tkinter import *
from tkinter import messagebox as tkMessageBox
from tkinter import simpledialog
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime

STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

window = None

class Minesweeper:

    # DBC: Preconditions:
    #   - tk  is a valid Tk instance.
    # Postconditions:
    #   - Initializes self.images with required image
    #   - Initial game frame is created and packed.
    #   - Calls restart() and updateTimer() to start the game.
    def init(self, tk):

        # import images
        self.images = {
            "plain": PhotoImage(file="images/tile_plain.gif"),
            "clicked": PhotoImage(file="images/tile_clicked.gif"),
            "mine": PhotoImage(file="images/tile_mine.gif"),
            "flag": PhotoImage(file="images/tile_flag.gif"),
            "wrong": PhotoImage(file="images/tile_wrong.gif"),
            "numbers": []
        }
        for i in range(1, 8+1):
            self.images["numbers"].append(PhotoImage(file="images/tile_"+str(i)+".gif"))

        # set up frame
        self.tk = tk
        self.frame = Frame(self.tk)
        self.frame.pack()

        self.restart()  # start game
        self.updateTimer()  # init timer

    # DBC: Preconditions:
    #   - self.size_x, self.size_y, self.num_mines, self.num_treasures are defined.
    # Postconditions:
    #   - Fills self.tiles with tile data structures.
    #   - tile button is created and assigned in the grid.
    #   - Rrandomly assigns mine_coords and treasure_coords.
    def setup(self):
        # create flag and clicked tile variables
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None

        # generate list of all cell coordinates
        cell_coords = [(x, y) for x in range(self.size_x) for y in range(self.size_y)]
        random.shuffle(cell_coords)

        mine_coords = cell_coords[:self.num_mines]
        treasure_coords = cell_coords[self.num_mines:self.num_mines + self.num_treasures]

        # create buttons
        self.tiles = dict({})
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                if y == 0:
                    self.tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = (x, y) in mine_coords
                isTreasure = (x, y) in treasure_coords

                gfx = self.images["plain"]

                tile = {
                    "id": id,
                    "isMine": isMine,
                    "isTreasure": isTreasure,
                    "state": STATE_DEFAULT,
                    "coords": {"x": x, "y": y},
                    "button": Button(self.frame, image=gfx),
                    "mines": 0  # calculated after grid is built
                }

                tile["button"].bind(BTN_CLICK, self.onClickWrapper(x, y))
                tile["button"].bind(BTN_FLAG, self.onRightClickWrapper(x, y))
                tile["button"].grid(row=x+1, column=y)  # offset by 1 row for timer

                self.tiles[x][y] = tile

        # loop again to find nearby mines and display number on tile
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                mc = 0
                for n in self.getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                self.tiles[x][y]["mines"] = mc

    # DBC: Preconditions:
    #   - Minesweeper object is properly initialized with Tk instance.
    # Postconditions:
    #   - Existing frame destroyed.  
    #   - A new frame created.
    #   - Prompts the user to select a difficulty level ("beginner", "intermediate", "expert").
    #   - Set up the size_x, size_y, num_mines, and num_treasures according to the selected difficulty level.
    #   - UI labels are refreshed.
    def restart(self):
        # destroy existing frame
        self.frame.destroy()
        # create new frame
        self.frame = Frame(self.tk)
        self.frame.pack()

        # Prompt the user to select level
        level = simpledialog.askstring("Select Level", "Enter level (beginner, intermediate, expert):")
        if level.lower() == 'beginner':
            self.size_x = 8
            self.size_y = 8
            self.num_mines = 10
            self.num_treasures = 1
        elif level.lower() == 'intermediate':
            self.size_x = 16
            self.size_y = 16
            self.num_mines = 40
            self.num_treasures = 3
        elif level.lower() == 'expert':
            self.size_x = 30
            self.size_y = 16
            self.num_mines = 99
            self.num_treasures = 5
        else:
            # default to beginner if input is invalid
            self.size_x = 8
            self.size_y = 8
            self.num_mines = 10
            self.num_treasures = 1

        # create labels/UI
        self.labels = {
            "time": Label(self.frame, text="00:00:00"),
            "mines": Label(self.frame, text="Mines: " + str(self.num_mines)),
            "flags": Label(self.frame, text="Flags: 0")
        }
        self.labels["time"].grid(row=0, column=0, columnspan=self.size_y)  # top full width
        self.labels["mines"].grid(row=self.size_x+1, column=0, columnspan=int(self.size_y/2))  # bottom left
        self.labels["flags"].grid(row=self.size_x+1, column=int(self.size_y/2)-1, columnspan=int(self.size_y/2))  # bottom right

        self.setup()
        self.refreshLabels()

    # DBC: Preconditions:
    #   - self.flagCount be an integer.
    #   - self.num_mines be an integer.
    # Postconditions:
    #   - The "flags" and "mines" lable is updated to show the current "self.flagCount" and "self.num_mines".
    def refreshLabels(self):
        self.labels["flags"].config(text="Flags: " + str(self.flagCount))
        self.labels["mines"].config(text="Mines: " + str(self.num_mines))

    # DBC: Preconditions:
    #   - "won" a boolean expression, indicates whether the player won or lost.
    # Postconditions:
    #   - All tiles are visible ("mines", "treasures", and "incorrect flags").
    #   - Appears a message box asking, the user wants to play again or not.
    #   - If the user selects "yes", the game restarts again; if "no", the application closes.
    def gameOver(self, won):
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                tile = self.tiles[x][y]
                if tile["isTreasure"]:
                    tile["button"].config(image=self.images["mine"])  # using existing image
                elif tile["isMine"] == False and tile["state"] == STATE_FLAGGED:
                    tile["button"].config(image=self.images["wrong"])
                elif tile["isMine"] == True and tile["state"] != STATE_FLAGGED:
                    tile["button"].config(image=self.images["mine"])

        self.tk.update()

        msg = "You Win! Play again?" if won else "You Lose! Play again?"
        res = tkMessageBox.askyesno("Game Over", msg)
        if res:
            self.restart()
        else:
            self.tk.quit()

    # DBC: Preconditions:
    #   - self.startTime may be "None", if game not started.
    # Postconditions:
    #   - self.updateTimer to updated time label after every 100 ms.
    #   - If game is on, shows the time elapsed since self.startTime.
    def updateTimer(self):
        ts = "00:00:00"
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            ts = str(delta).split('.')[0]  # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts  # zero-pad
        self.labels["time"].config(text=ts)
        self.frame.after(100, self.updateTimer)

    # DBC: Preconditions:
    #   - x, y are valid indexes within the game board.
    # Postconditions:
    #   - Returns a list of neighbor tiles around (x, y).
    #   - Excludes, if the tiles is out of range.
    def getNeighbors(self, x, y):
        neighbors = []
        coords = [
            {"x": x-1,  "y": y-1},  # top left
            {"x": x-1,  "y": y},    # top middle
            {"x": x-1,  "y": y+1},  # top right
            {"x": x,    "y": y-1},  # left
            {"x": x,    "y": y+1},  # right
            {"x": x+1,  "y": y-1},  # bottom left
            {"x": x+1,  "y": y},    # bottom middle
            {"x": x+1,  "y": y+1},  # bottom right
        ]
        for n in coords:
            try:
                neighbors.append(self.tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors

    # DBC: Preconditions:
    #   - x, y are valid tile coordinate within the game board.
    # Postconditions:
    #   - Returns a lambda function that calls "onClick" with a valid (x, y).
    def onClickWrapper(self, x, y):
        return lambda Button: self.onClick(self.tiles[x][y])

    # DBC: Preconditions:
    #   - x, y are valid tile coordinate within the game board.
    # Postconditions:
    #   - Returns a lambda function that calls "onRightClick" with a valid (x, y).
    def onRightClickWrapper(self, x, y):
        return lambda Button: self.onRightClick(self.tiles[x][y])

    # DBC: Preconditions:
    #   - x, y are valid tile dictionary with keys {"isMine", "isTreasure", "mines"}.
    #   - game.state is RUNNING.
    # Postconditions:
    #   - If tile.isTreasure == True, call gameOver(True).
    #   - If tile.isMine == True, call gameOver(False).
    #   - If tile.mines == 0, clear surrounding tiles.
    #   - Otherwise, set tile as visible.
    #   - If all safe tiles are clicked, call gameOver(True).
    def onClick(self, tile):
        if self.startTime == None:
            self.startTime = datetime.now()

        if tile["isTreasure"]:
            tile["button"].config(image=self.images["mine"])
            self.gameOver(True)
            return

        if tile["isMine"] == True:
            self.gameOver(False)
            return

        if tile["mines"] == 0:
            tile["button"].config(image=self.images["clicked"])
            self.clearSurroundingTiles(tile["id"])
        else:
            tile["button"].config(image=self.images["numbers"][tile["mines"]-1])

        if tile["state"] != STATE_CLICKED:
            tile["state"] = STATE_CLICKED
            self.clickedCount += 1
        if self.clickedCount == (self.size_x * self.size_y) - self.num_mines - self.num_treasures:
            self.gameOver(True)

    # DBC: Preconditions:
    #   - tile is a dictionary with keys {isMine, isTreasure, mines}.
    #   - game.state is RUNNING.
    # Postconditions:
    #   - If tile.state == DEFAULT, set FLAGGED, increment flagCount, adjust correctFlagCount.
    #   - If tile.state == FLAGGED, set DEFAULT, decrement flagCount, adjust correctFlagCount.
    #   - Refresh UI labels.
    def onRightClick(self, tile):
        if self.startTime == None:
            self.startTime = datetime.now()

        if tile["state"] == STATE_DEFAULT:
            tile["button"].config(image=self.images["flag"])
            tile["state"] = STATE_FLAGGED
            tile["button"].unbind(BTN_CLICK)
            if tile["isMine"] == True:
                self.correctFlagCount += 1
            self.flagCount += 1
            self.refreshLabels()
        elif tile["state"] == 2:  # STATE_FLAGGED
            tile["button"].config(image=self.images["plain"])
            tile["state"] = 0  # STATE_DEFAULT
            tile["button"].bind(BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
            if tile["isMine"] == True:
                self.correctFlagCount -= 1
            self.flagCount -= 1
            self.refreshLabels()

    # DBC: Preconditions:
    #   id = "x_y", where x and y are valid coordinates
    # Postconditions:
    #   clear all reachable tiles with mines == 0
    #   make edge tiles with mines > 0 visible
    def clearSurroundingTiles(self, id):
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in self.getNeighbors(x, y):
                self.clearTile(tile, queue)

    # DBC: Preconditions:
    #   - tile is a dictionary with keys {id, state, mines}.
    #   - queue is a deque used by clearSurroundingTiles.
    # Postconditions:
    #   - If tile.state == DEFAULT and tile.mines == 0, set visible, add to queue.
    #   - If tile.state == DEFAULT and tile.mines > 0, set visible.
    #   - Increment clickedCount for state change to CLICKED.
    def clearTile(self, tile, queue):
        if tile["state"] != STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            tile["button"].config(image=self.images["clicked"])
            queue.append(tile["id"])
        else:
            tile["button"].config(image=self.images["numbers"][tile["mines"]-1])

        tile["state"] = STATE_CLICKED
        self.clickedCount += 1

### END OF CLASSES ###

# DBC: Preconditions:
#   - None.
# Postconditions:
#   - Creates a Tk root window.
#   - Initializes Minesweeper object.
#   - Runs the GUI main loop.
def main():
    # create Tk instance
    window = Tk()
    # set program title
    window.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(window)
    # run event loop
    window.mainloop()

if __name__ == "__main__":
    main()