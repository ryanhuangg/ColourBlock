"""Author: Long Uy Nguyen"""

from block import Block
from node import Node
from grid import Grid
from typing import List


class SquareBlock(Block):
    """
    Represent a 2x2 square block with following (*) nodes location
    * *
    * *
    default colour is (0, 255, 255)
    Take in the list of nodes in grid as parameter to render this block
    """
    _nodes = List[Node]  # List of nodes of this SquareBlock

    def __init__(self, g: Grid):
        colour = (0, 255, 255)
        super().__init__("Square Block", colour, g.get_nodes())
        self.initialize_nodes()

    def initialize_nodes(self):
        """
        Create the SquareBlock object with nodes
        """
        node1 = self.grid[0][4]
        node2 = self.grid[1][4]
        node3 = self.grid[0][5]
        node4 = self.grid[1][5]
        self._nodes = [node1, node2, node3, node4]
        for node in self._nodes:
            node.set_colour(self.colour)

    def move_left(self):
        """
        Move this SquareBlock to the left
        """
        for node in self._nodes:
            self._move_node_left(node)

    def _move_node_left(self, node):
        """
        Move the node of this SquareBlock to the left
        :param node: Node
        """
        for l in range(len(self.grid)):
            for n in range(len(self.grid[l])):
                if self.grid[l][n] == node:
                    try:  # If possible to traverse left, then make the change
                        # and set the node's status appropriately
                        index = self._nodes.index(node)
                        self.grid[l][n-1].set_colour(self.colour)
                        self.grid[l][n].reset_colour()
                        self._nodes[index] = self.grid[l][n-1]
                        self.grid[l][n-1].set_control(True)
                        self.grid[l][n].set_control(False)
                        return
                    except IndexError:
                        continue

    def _move_node_right(self, node):
        """
        Move the node of this SquareBlock to the right
        :param node: Node
        """
        for l in range(len(self.grid)):
            for n in range(len(self.grid[l])):
                if self.grid[l][n] == node:
                    try:  # If possible to traverse right, then make the change
                        # and set the node's status appropriately
                        index = self._nodes.index(node)
                        self.grid[l][n+1].set_colour(self.colour)
                        self.grid[l][n].reset_colour()
                        self._nodes[index] = self.grid[l][n+1]
                        self.grid[l][n+1].set_control(True)
                        self.grid[l][n].set_control(False)
                        return
                    except IndexError:
                        continue

    def move_right(self):
        """
        Move this SquareBlock to the right
        """
        for node in self._nodes:
            self._move_node_right(node)

    def _move_node_down(self, node):
        """
        Move the SquareBlock's node down 1 row
        :param node: Node
        """
        for l in range(len(self.grid)):
            for n in range(len(self.grid[l])):
                if self.grid[l][n] == node:
                    try:  # If possible to traverse down, then make the change
                        # and set the node's status appropriately
                        index = self._nodes.index(node)
                        self.grid[l+1][n].set_colour(self.colour)
                        self.grid[l][n].reset_colour()
                        self._nodes[index] = self.grid[l+1][n]
                        self.grid[l+1][n].set_control(True)
                        self.grid[l][n].set_control(False)
                        return
                    except IndexError:
                        continue

    def traverse_down_1row(self):
        """
        Move the SquareBlock down 1 row
        """
        for node in self._nodes:
            self._move_node_down(node)

    def rotate(self):
        """
        Requires implementation
        Rotate the block 90 degree clockwise
        """
        pass
