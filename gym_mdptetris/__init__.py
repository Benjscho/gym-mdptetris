from gym.envs.registration import register

register(
    id='mdptetris-v0',
    entry_point='gym_mdptetris.envs:Tetris'
)