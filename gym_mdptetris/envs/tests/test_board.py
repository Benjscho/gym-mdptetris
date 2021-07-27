import unittest
from gym_mdptetris.envs.board import Board
from gym_mdptetris.envs.piece import Piece



class BoardTests(unittest.TestCase):
    def test_default_board_init(self):
        b = Board()
    
    def test_board_limits(self):
        b = Board(max_piece_height=4, width=10, height=20)

    def test_drop_piece(self):
        b = Board(max_piece_height=4, width=10, height=20)
        L = """X\nX\nXX"""
        p = Piece(4,3,2,L)
        b.drop_piece(p.orientations[0], 1, True)
        b.cancel_last_move()
