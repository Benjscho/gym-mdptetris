import gym
import numpy as np

from gym_mdptetris.envs.tetris import Tetris, MelaxTetris

env = MelaxTetris()
for i in range(10):
	action = env.action_space.sample()
	print(action)
	obs, reward, done, info = env.step(action)
	env.render()
	#print(reward)
	if done: break