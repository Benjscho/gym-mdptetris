import unittest
from gym_mdptetris.envs.board import Board

class BoardTests(unittest.TestCase):
    def test_default_board_init(self):
        b = Board()
    
    def test_board_limits(self):
        b = Board(max_piece_height=4, width=10, height=20)