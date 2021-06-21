import unittest
import gym_mdptetris.envs.piece as piece
import gym_mdptetris.envs.binary_piece as binary_piece

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
    
    def test_piece_type(self):
        with self.assertRaises(TypeError):
            l = piece.Piece(4, 3, 2, 1)

    def test_empty_piece(self):
        with self.assertRaises(ValueError):
            l = piece.Piece(4, 3, 2, "")

class BinaryPieceTests(unittest.TestCase):
    def test_import(self):
        l_piece = binary_piece.BinaryPiece(4, 3, 2, L)
        O_piece = binary_piece.BinaryPiece(1, 2, 2, O)
        
    def test_class(self):
        l = binary_piece.BinaryPiece(4, 3, 2, L)
        self.assertIsInstance(l.orientations[0], binary_piece.BinaryPieceOrientation)
        self.assertIsInstance(l, binary_piece.BinaryPiece)

    def test_orientation_error(self):
        with self.assertRaises(ValueError):
            l = binary_piece.BinaryPiece(5, 3, 2, L)
        with self.assertRaises(ValueError):
            l = binary_piece.BinaryPiece(-1, 3, 2, L)
        with self.assertRaises(ValueError):
            l = binary_piece.BinaryPiece(4, -3, 2, L)
        with self.assertRaises(ValueError):
            l = binary_piece.BinaryPiece(4, 3, -2, L)
    
    def test_piece_type(self):
        with self.assertRaises(TypeError):
            l = binary_piece.BinaryPiece(4, 3, 2, 1)

    def test_empty_piece(self):
        with self.assertRaises(ValueError):
            l = binary_piece.BinaryPiece(4, 3, 2, "")

if __name__=='__main__':
    unittest.main()