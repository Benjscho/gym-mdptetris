import unittest
import piece

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
        pass