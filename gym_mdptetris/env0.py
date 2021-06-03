import piece
import gym
import numpy as np

from gym import Env, spaces

class Tetris0(Env):
    def __init__(self):
        super(Tetris0, self).__init__()
        pass

    def step(self):
        pass
    
    def reset(self):
        pass

    def render(self):
        pass

    def load_pieces(self, piece_file):
        f = open(piece_file, "rt")
        pieces = [] 
        
        lines = f.readlines()
        for line in lines:
            if line[0] == '#':
                lines.remove(line)
        nb_pieces = int(line[0])

        curr_line = 1 
        for i in range(nb_pieces):
            nb_orientations, height, width = map(int, lines[curr_line])
            shape = ""
            for j in range(curr_line + 1, curr_line + height):
                shape += lines[j]
            pieces.append(piece.Piece(nb_orientations, height, width, shape))
            curr_line += 1 + height 

        return pieces

