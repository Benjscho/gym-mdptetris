import unittest
import gym_mdptetris.envs.board as board
import gym_mdptetris.envs.piece as piece
import gym_mdptetris.envs.feature_functions as f 

O = """
XX
XX
"""

L = """
X
X
XX
"""

class featureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run expensive functions that need to be done before all other class tests"""
        cls.l = piece.Piece(4, 3, 2, L)
        cls.o = piece.Piece(1, 2, 2, O)
        cls.board = board.Board()

    def test_landing_height(self):
        self.board.reset()
        self.board.drop_piece(self.l.orientations[0], 0)
        self.assertEqual(f.get_landing_height(self.board), 1)
        self.board.drop_piece(self.l.orientations[0], 0)
        self.assertEqual(f.get_landing_height(self.board), 4)
        self.board.reset()
        
        self.board.drop_piece(self.o.orientations[0], 0)
        self.assertEqual(f.get_landing_height(self.board), 0.5)
        self.board.drop_piece(self.o.orientations[0], 0)
        self.assertEqual(f.get_landing_height(self.board), 2.5)
        self.board.reset()

    def test_eroded_cells(self):
        self.board.reset()
        self.board.drop_piece(self.o.orientations[0], 0)
        self.board.drop_piece(self.o.orientations[0], 2)
        self.board.drop_piece(self.o.orientations[0], 4)
        self.board.drop_piece(self.o.orientations[0], 6)
        self.board.drop_piece(self.o.orientations[0], 8)
        self.assertEqual(f.get_eroded_cells(self.board), 8)
        self.board.reset()

    def test_row_transitions(self):
        self.board.reset()
        self.assertEqual(f.get_row_transitions(self.board), 40)
        self.board.drop_piece(self.o.orientations[0], 0)
        self.board.drop_piece(self.o.orientations[0], 2)
        self.board.drop_piece(self.o.orientations[0], 6)
        self.assertEqual(f.get_row_transitions(self.board), 44)
        self.board.drop_piece(self.o.orientations[0], 4)
        self.assertEqual(f.get_row_transitions(self.board), 40)
        self.board.reset()

    def test_col_transitions(self):
        self.board.reset()
        self.assertEqual(f.get_col_transitions(self.board), 10)
        self.board.drop_piece(self.l.orientations[0], 0)
        self.board.drop_piece(self.l.orientations[0], 2)
        self.board.drop_piece(self.l.orientations[0], 6)
        self.assertEqual(f.get_col_transitions(self.board), 16)
        self.board.drop_piece(self.o.orientations[0], 4)
        self.assertEqual(f.get_col_transitions(self.board), 16)
        self.board.reset()

    def test_holes(self):
        self.board.reset()
        self.assertEqual(f.get_holes(self.board), 0)
        self.board.drop_piece(self.l.orientations[0], 0)
        self.board.drop_piece(self.l.orientations[0], 2)
        self.board.drop_piece(self.l.orientations[0], 6)
        self.assertEqual(f.get_holes(self.board), 6)
        self.board.drop_piece(self.o.orientations[0], 4)
        self.assertEqual(f.get_holes(self.board), 6)
        self.board.reset()

    def test_well_sums(self):
        self.board.reset()
        self.assertEqual(f.get_well_sums(self.board), 0)
        self.board.drop_piece(self.l.orientations[0], 0)
        self.board.drop_piece(self.l.orientations[0], 2)
        self.board.drop_piece(self.l.orientations[0], 6)
        self.assertEqual(f.get_well_sums(self.board), 2)
        self.board.drop_piece(self.o.orientations[0], 4)
        self.assertEqual(f.get_well_sums(self.board), 4)
        self.board.drop_piece(self.l.orientations[0], 8)
        self.assertEqual(f.get_well_sums(self.board), 8)
        self.board.reset()