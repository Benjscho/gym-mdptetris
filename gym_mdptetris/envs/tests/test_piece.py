import unittest
import gym_mdptetris.envs.piece as piece

O = """
XX
XX
"""

L = """
X
X
XX
"""

class pieceTests(unittest.TestCase):
    def test_import(self):
        l_piece = piece.Piece(4, 3, 2, L)
        O_piece = piece.Piece(1, 2, 2, O)
        
    def test_class(self):
        l = piece.Piece(4, 3, 2, L)
        self.assertIsInstance(l.orientations[0], piece.PieceOrientation)
        self.assertIsInstance(l, piece.Piece)

    def test_orientation_error(self):
        with self.assertRaises(ValueError):
            l = piece.Piece(5, 3, 2, L)
        with self.assertRaises(ValueError):
            l = piece.Piece(-1, 3, 2, L)
        with self.assertRaises(ValueError):
            l = piece.Piece(4, -3, 2, L)
        with self.assertRaises(ValueError):
            l = piece.Piece(4, 3, -2, L)

if __name__=='__main__':
    unittest.main()