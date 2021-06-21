import gym_mdptetris.envs.binary_piece as piece

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