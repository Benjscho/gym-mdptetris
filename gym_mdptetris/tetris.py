import gym
import piece
import board
import os 
import numpy as np

from gym import Env, spaces

class Tetris(Env):
    def __init__(self, seed=12345):
        super(Tetris, self).__init__()
        pieces_path = os.path.dirname(os.path.abspath(__file__)) + '/data/pieces4.dat'
        self.pieces, self.nb_pieces = self.load_pieces(pieces_path)
        max_piece_height = 0
        for piece in self.pieces:
            for o in piece.orientations:
                max_piece_height = max(max_piece_height, o.height)
        self.board = board.Board(max_piece_height)
        self.current_piece = 0
        self.generator = np.random.default_rng()
        # Action space is the board width multiplied by the max number of piece orientations, 
        # zero indexed (so less 1). 
        self.action_space = np.array([i for i in range((self.board.width * 4) - 1)])

    def step(self, action: int):
        done = False
        if action not in self.action_space:
            raise ValueError("Action not in action space.")
        orientation = (action // 10) % self.pieces[self.current_piece].nb_orientations
        column = (action % 10) + 1
        column = min(column, self.board.width - self.pieces[self.current_piece].orientations[orientation].width + 1)
        reward = self.board.drop_piece(self.pieces[self.current_piece].orientations[orientation], column)
        if self.board.wall_height > self.board.height:
            done = True
        self.current_piece = self.generator.choice(self.nb_pieces)
        return self.get_state(), reward, done, {}
    
    def reset(self):
        self.board.reset()
        self.current_piece = self.generator.choice(self.nb_pieces)
        return self.get_state()

    def get_state(self):
        return np.array([self.board.board, self.pieces[self.current_piece].orientations[0].shape], dtype=object)

    def render(self, mode='human'):
        print("Current piece:")
        print(self.pieces[self.current_piece])
        print(self.board)
        

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

