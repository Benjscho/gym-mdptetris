import unittest
import gym
from gym_mdptetris.envs.tetris import Tetris

class TetrisTests(unittest.TestCase):
    def test_env_init(self):
        env = Tetris()

    def test_env_board(self):
        env = Tetris()
        
class GymTests(unittest.TestCase):
    def test_gym_make(self):
        env = gym.make('gym_mdptetris:mdptetris-v0')