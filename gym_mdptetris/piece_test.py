import unittest
import piece
import board
import env0

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

    board = board.Board()
    print(board)
    board.drop_piece(p.orientations[2], 1, False)
    print(board)
    board.drop_piece(p.orientations[2], 3, False)
    print(board)
    board.drop_piece(p.orientations[2], 5, False)
    print(board)
    board.drop_piece(p.orientations[2], 7, False)
    print(board)
    res = board.drop_piece(p.orientations[2], 9, False)
    print(board)

    #print(p)

    env = env0.Tetris0()
    pieces, nb_pieces = env.load_pieces('data/pieces_melax.dat')
    for piece in pieces:
        print(piece)