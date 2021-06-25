from gym.envs.registration import register

register(
    id='mdptetris-v0',
    entry_point='gym_mdptetris.envs:Tetris'
)

register(
    id='mdptetris-v1',
    entry_point='gym_mdptetris.envs:TetrisFlat'
)

register(
    id='melaxtetris-v0',
    entry_point='gym_mdptetris.envs:MelaxTetris'
)

register(
    id='melaxtetris-v1',
    entry_point='gym_mdptetris.envs:MelaxTetrisFlat'
)