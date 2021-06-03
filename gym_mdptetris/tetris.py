import gym
import piece
import board
import numpy as np


from gym import Env, spaces

class Tetris(Env):
    def __init__(self, seed=12345):
        super(Tetris0, self).__init__()
        self.pieces, self.nb_pieces = self.load_pieces('data/pieces4.dat')
        max_piece_height = 0
        for piece in self.pieces:
            for o in piece.orientations:
                max_piece_height = max(max_piece_height, o.height)
        self.board = board.Board(max_piece_height)
        self.current_piece = 0
        self.generator = np.random.default_rng()

    def step(self, action):
        pass
    
    def reset(self):
        self.board.reset()
        self.current_piece = self.generator.choice(self.nb_pieces)
        return np.array([self.board.board, self.pieces[self.current_piece].orientations[0].shape])

    def get_state(self):
        return np.array([self.board.board, self.pieces[self.current_piece].orientations[0].shape])

    def render(self):
        pass

    def load_pieces(self, piece_file):
        f = open(piece_file, "rt")
        pieces = [] 
        
        lines = f.readlines()
        i = 0
        while i < len(lines):
            if lines[i][0] == '#':
                del lines[i]
            else:
                i += 1 
        nb_pieces = int(lines[0])

        curr_line = 1 
        for i in range(nb_pieces):
            nb_orientations, height, width = map(int, lines[curr_line].split())
            shape = ""
            for j in range(curr_line + 1, curr_line + height + 1):
                shape += lines[j]
            pieces.append(piece.Piece(nb_orientations, height, width, shape))
            curr_line += 1 + height 

        return pieces, nb_pieces

