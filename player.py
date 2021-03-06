from typing import List, Dict, Tuple
from grid import Grid
from visuals import Visuals
from random import randint as rand
import pygame

# import all the blocks
import block
import iblock
import l_oppositeblock
import lblock
import squareblock
import tblock
import z_oppositeBlock
import zblock

""" ===== CONSTANTS ===== """

""" === ORIGIN ==="""
ORIGIN = (0, 0)

""" === Resolution === """
WIDTH = 400 # 1024 #
HEIGHT = 600 # 768 #

""" === FONT === """
FONT = 'Consolas'

""" === CLOCK SPEED === """
TICK_LENGTH = 775

""" === BACKGROUND COLOUR ==="""
COLOUR = (0, 32, 64)

""" === PADDING === """
PADDING = 5

""" === Move Delay === """
DELAY = 50

""" === Drop Factor === """
FACTOR = 10

""" Author: Pranshu Patel """
class Player:

    """ PLAYER CLASS
        This class represents a character/player in the game.
        It keeps track of the score and updates the score as
        the game is played.
        === Private Attributes ===
        _name - The name of the character.
        _time - The amount of seconds the character has been in the game.
        _score - The current score of the character.
        _block - The current block that the character is in control of.
        _grid - The grid that the current game is using
        _vis - The visuals for the game
        _has_lost - whether the game is finished (ie user lost)
        _has_quit - whether the user has quit the game
        _last_block - the int id of the last block spawned
     """
    _name: str
    _time: int
    _score: int
    _block: block.Block
    _grid: Grid
    _vis: Visuals
    _has_lost: bool
    _has_quit: bool
    _last_block: int

    def __init__(self, name: str, time: int):
        """Initialize the new character entering the game.
           Then start the game.
        """
        self._name = name
        self._time = time
        self._score = 0
        self._history = []
        self._vis = Visuals(WIDTH, HEIGHT, TICK_LENGTH, FONT, self, DELAY, FACTOR)
        self._block = None
        self._has_lost = False
        self._has_quit = False
        self._last_block = -1
        self.setup_grid()
        self.start_game()

    def setup_grid(self):
        """ Create an instance of grid for this player to use """
        # To centre, take the centre of the screen, then subtract
        # the grid's width (which is HEIGHT // 2).
        left_offset = (WIDTH - (HEIGHT // 2)) // 2
        self._grid = Grid(WIDTH, HEIGHT, PADDING, COLOUR, left_offset)

    def start_game(self):
        """ Start pygame with this game. """
        print("starting game")
        self.create_block()

        self._vis.play(self._grid)


    def get_name(self) -> str:
        """ Return the name of this character. """
        return self._name

    def get_score(self) -> int:
        """ Return the current character's score. """
        return self._score

    def get_history(self) -> List[int]:
        """ Return the history of the character. """

        return self._history

    def get_grid(self) -> Grid:
        """ Return a copy of the grid. """
        return self._grid

    def has_lost(self) -> bool:
        """ Return whether the user has lost this game yet. """
        return self.has_lost

    def has_quit(self) -> bool:
        """ Return whether the user has quit. """
        return self._has_quit

    def update_score(self) -> None:
        """ Update the current score of the current character to
        match the score of the character's grid. """

        self._score = self._grid.get_score()

    def move_block_left(self):
        """ Move the current block to the left by 1 unit. """
        if self._can_move(dir=-1):
            self._block.move_left()

    def move_block_right(self):
        """ Move the current block to the right by 1 unit. """
        if self._can_move(dir=1):
            self._block.move_right()

    def _can_move(self, dir=0) -> bool:
        """ Return true if the block can move in given direction.
            -1 means left, 1 means right.
            This stops the block from wrapping the grid,
            i.e. moving from col 0 to col 9.
        """
        if not (dir == 1 or dir == -1):
            return False

        block = self._block._nodes
        grid = self._grid.get_nodes()

        # move_dict maps -1 to left column, 1 to right column
        move_dict = {-1:0, 1:9}

        # Check if node hits walls
        for n in block:
            pos = n.get_coords()
            # If x coordinate is 0 or 9, stop moving left / right
            if pos[0] == move_dict[dir]:
                return False
            # If the node to the left or right is occupied, do not move into it
            if grid[pos[1]][pos[0] + dir].get_filled():
                return False

        return True

    def rotate_block(self):
        """ Rotate the current block 90 degrees clockwise. """
        self.rotate()

    def create_block(self) -> None:
        """ Spawn in a random block in the
            top rows of the grid.
        """
        # DO NOT MAKE A NEW BLOCK
        # UNTIL THE OLD ONE IS GONE.
        if self._block:
            return

        # Ensure that the new block is not the same as previous block.
        block_type = self._last_block
        while block_type == self._last_block:
            # ex. If type is chosen to be 0, only accept if last block was not 0
            block_type = rand(0, 6)

        self._last_block = block_type
        # Begin switch case
        if block_type == 0:
            self._block = iblock.IBlock(self._grid)
        elif block_type == 1:
            self._block = l_oppositeblock.L_oppositeBlock(self._grid)
        elif block_type == 2:
            self._block = lblock.LBlock(self._grid)
        elif block_type == 3:
            self._block = squareblock.SquareBlock(self._grid)
        elif block_type == 4:
            self._block = tblock.TBlock(self._grid)
        elif block_type == 5:
            self._block = z_oppositeBlock.Z_oppositeBlock(self._grid)
        elif block_type == 6:
            self._block = zblock.ZBlock(self._grid)

        self.set_block_control(True)
        # print("block: ", self._block._name)

    def play_move(self, move=0, rotate=False) -> None:
        """ Play one move in the game.

            The parameter move represents the player's move direction:
            -1: move block left
             1: move block right
             anything else do nothing

            rotate: if true, rotate the block
        """
        if not self._block:
            print("no block")
            return

        if move == -1:
            self.move_block_left()
        elif move == 0:
            self._block.rotate()
        elif move == 1:
            self.move_block_right()

    def block_fall(self):
        """ Move the current block down by 1 row
            if it can. Otherwise, make a new block.
            Afterwards, check if lines are full.
        """

        # Check if any lines are filled
        self.clear_lines()

        self.set_block_control(True)
        self.set_block_filled(True)

        # Do nothing if there is no block
        if not self._block:
            return

        # NOTE: check if block can move down
        lowest_y = 0
        # Store ref to grid's background colour for later
        colour = self._grid.get_colour()
        grid_nodes = self._grid.get_nodes()

        for node in self._block._nodes:
            # Get pos from the node
            # NOTE: pos is in pixel coordinates
            pos = node.get_coords()
            x = pos[0]
            y = pos[1]

            # NOTE: int div to round down
            if y >= 23:
                # Bottom of grid, do not go down
                # Stop control of block
                self.set_block_control(False)
                self.set_block_filled(True)
                self._block = None
                self.create_block()
                return

            # Check the nodes below if block can fall
            below = grid_nodes[y+1][x]
            if (not below.get_in_control()) and \
                below.get_colour() != colour:
                # Node below is not this block
                # and occupied

                # node.colour = (0,0,0)
                # below.colour = (255,255,255)

                self.set_block_control(False)
                self.set_block_filled(True)
                self._block = None

                # CHECK IF GAME IS OVER
                # If a block that high collides, the game is over
                if y <= 2:
                    self._grid.set_game_over()

                self.create_block()
                return

        if self._block:
            self.set_block_control(False)
            self.set_block_filled(False)
            self._block.traverse_down_1row()

    def clear_lines(self) -> None:
        """ Check if any lines are full on the grid.
            The grid will clear them for us and update the score.
            Then we update the score in this class
            and update the drop speed of the blocks.
        """
        self._grid.clear_lines()
        self.update_score()
        tick_update = self.get_score() // 20
        if tick_update > 13: tick_update = 13
        if (TICK_LENGTH - DELAY*tick_update) > 0:
            self._vis.update_tick(TICK_LENGTH - DELAY*tick_update)

    def set_block_control(self, status) -> None:
        """ Set the status of each node of the curr
            block to <status>.
        """
        if not self._block:
            return

        for i in range(len(self._block._nodes)):
            self._block._nodes[i].set_control(status)

    def set_block_filled(self, status) -> None:
        """ Set the filled status of each node of
            the curr block to <status>.
        """
        if not self._block:
            return

        for i in range(len(self._block._nodes)):
            self._block._nodes[i].set_filled(status)

    def lose(self, restart=True) -> None:
        """ Signify this user has lost this game.
            No moves are possible at this point.
        """
        self._has_lost = True
        if not restart:
            # User does not want to restart
            self._has_quit = True
