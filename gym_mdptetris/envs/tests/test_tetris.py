import unittest
import gym
from gym_mdptetris.envs.tetris import Tetris

class TetrisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run expensive functions that need to be done before all other class tests"""
        cls._env = Tetris()
        

    def test_env_init(self):
        env = Tetris()

    def test_env_board(self):
        env = Tetris()

    def test_piece_file(self):
        env = Tetris()
    
    def test_state_obs_space(self):
        self.assertEqual(self._env.get_state().shape, self._env.observation_space.shape)

class GymTests(unittest.TestCase):
    def test_gym_make(self):
        env = gym.make('gym_mdptetris:mdptetris-v0')