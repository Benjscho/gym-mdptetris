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

    board = piece.Board()
    board.print_board()
    board.drop_piece(p.orientations[2], 1, False)
    board.print_board()
    board.drop_piece(p.orientations[2], 3, False)
    board.print_board()
    board.drop_piece(p.orientations[2], 5, False)
    board.print_board()
    board.drop_piece(p.orientations[2], 7, False)
    board.print_board()
    res = board.drop_piece(p.orientations[2], 9, False)
    board.print_board()