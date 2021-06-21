import gym_mdptetris.envs.binary_piece as piece
import gym_mdptetris.envs.binary_board as board
import gym_mdptetris.envs.binary_tetris as tetris
import timeit

S = """
XX
XX
"""

L = """
X
X
XX
"""

p = piece.BinaryPiece(4, 3, 2, L)
for o in p.orientations:
	print(o)

b = board.BinaryBoard()

print(b)

b.drop_piece(p.orientations[1], 1, False)
print(b)
b.drop_piece(p.orientations[0], 0, False)
print(b)

b.drop_piece(p.orientations[2], 4, False)
print(b)
b.drop_piece(p.orientations[3], 6, False)
print(b)

b.reset()

s = piece.BinaryPiece(1, 2, 2, S)

b.drop_piece(s.orientations[0], 0)
b.drop_piece(s.orientations[0], 2)
b.drop_piece(s.orientations[0], 4)
b.drop_piece(s.orientations[0], 6)
print(b)
r = b.drop_piece(s.orientations[0], 8)
print(b)
print(r)

env = tetris.BinaryTetris()
env.reset()
env.render()
env.step((0,0))
env.render()

print(timeit.timeit(stmt="env.step((0, 0)) \nenv.reset()", setup="import gym_mdptetris.envs.binary_tetris as tetris \nenv = tetris.BinaryTetris()", number=100000))