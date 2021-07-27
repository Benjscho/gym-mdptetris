import unittest
import numpy as np
import gym_mdptetris.envs.linear_game as l

class linearTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.l_g = l.LinearGame()

    def test_intialisation(self):
        l_g_t = l.LinearGame()

    def test_dellacherie_features(self):
        print(self.l_g.get_dellacherie_features())
    
    def test_play_game(self):
        self.l_g.weights = np.array([0,0,0,0,0,0])
        self.l_g.play_game()