import unittest
import gym
import numpy as np

from gym_mdptetris.envs.tetris import Tetris, MelaxTetris

class TetrisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run expensive functions that need to be done before all other class tests"""
        print("debugging")
        cls._env = Tetris()
        
    def test_env_init(self):
        env = Tetris()

    def test_env_board(self):
        env = Tetris()

    def test_piece_file(self):
        env = Tetris()

    def test_piecedrops(self):
        self._env.reset()
        for i in range(30):
            action = self._env.action_space.sample()
            obs, reward, done, info = self._env.step(action)
            if done: break
        self.assertEqual(done, True)

    def test_non_cancel_move(self):
        print("testing")
        obs = self._env.reset()
        action = self._env.action_space.sample()
        o, r, d, i = self._env.step(action)
        with self.assertRaises(AttributeError): 
            self._env.board.cancel_last_move()
        self._env.reset()


class MelaxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._env = MelaxTetris()

    def test_drop(self):
        self._env.reset()
        for i in range(10):
            action = self._env.action_space.sample()
            obs, reward, done, info = self._env.step(action)
            if done: break
            

class GymTests(unittest.TestCase):
    def test_gym_make(self):
        env = gym.make('gym_mdptetris:mdptetris-v0')
    
