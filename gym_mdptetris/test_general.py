import unittest
import piece
import board
import tetris

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

    board.drop_piece(p.orientations[0], 1, False)
    print(board)
    board.drop_piece(p.orientations[1], 3, False)
    print(board)
    board.drop_piece(p.orientations[2], 5, False)
    print(board)
    board.drop_piece(p.orientations[3], 7, False)
    print(board)

    #print(p)

    env = tetris.Tetris()
    pieces, nb_pieces = env.load_pieces('data/pieces4.dat')
    for piece in pieces:
        print(piece)
    
    env.reset()
    env.render()