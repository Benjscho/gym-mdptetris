import unittest
import os
import timeit
import gym_mdptetris.envs.piece as piece
import gym_mdptetris.envs.board as board
import gym_mdptetris.envs.tetris as tetris

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
    
    env.reset()
    env.render()
    
    # Test how long it takes to make 100,000 steps
    print(timeit.timeit(stmt="env.step(0) \nenv.reset()", setup="import tetris \nenv = tetris.Tetris()", number=100000))
