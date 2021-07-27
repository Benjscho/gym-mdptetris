import unittest
import os
import time
import timeit
import gym_mdptetris.envs.piece as piece
import gym_mdptetris.envs.board as board
import gym_mdptetris.envs.tetris as tetris


class SpeedTest(unittest.TestCase):

    def test_speed(self):

        L = """X\nX\nXX"""
        p = piece.Piece(4,3,2,L)

        b = board.Board()

        b.drop_piece(p.orientations[0], 1, False)
        b.drop_piece(p.orientations[1], 3, False)
        b.drop_piece(p.orientations[2], 5, False)
        b.drop_piece(p.orientations[3], 7, False)

        env = tetris.Tetris()
        
        env.reset()
        env.step((0,0))
        env.reset()
        # Test how long it takes to make 100,000 steps
        t = int(time.time())
        env.seed(t)

        setup = """import gym_mdptetris.envs.tetris as tetris\nimport time\nenv = tetris.Tetris()\nenv.seed(time.time())"""
        print(timeit.timeit(stmt="env.step((0, 0)) \nenv.reset()", setup=setup, number=10000))

