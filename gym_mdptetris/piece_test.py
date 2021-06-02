import unittest
import piece


S = """
XX
XX
"""

L = """
X
X
XX
"""

if __name__=="__main__":
    p = piece.Piece(4,3,2,L)
    for o in p.orientations:
        print(o)