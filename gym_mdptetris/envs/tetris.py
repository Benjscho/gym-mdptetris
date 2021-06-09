import gym
import os 
import gym_mdptetris.envs.piece as piece
import gym_mdptetris.envs.board as board
import numpy as np

from gym import Env, spaces

class Tetris(Env):
    def __init__(self, seed=12345):
        super(Tetris, self).__init__()
        pieces_path = os.path.dirname(os.path.abspath(__file__)) + '/data/pieces4.dat'
        self.pieces, self.nb_pieces = self.load_pieces(pieces_path)
        self.max_piece_height = 0
        for piece in self.pieces:
            for o in piece.orientations:
                self.max_piece_height = max(self.max_piece_height, o.height)
        self.board = board.Board(max_piece_height=self.max_piece_height)
        self.current_piece = 0
        self.generator = np.random.default_rng()
        # Observation is the representation of the current piece, concatenated with the board
        # Low is represented by the empty board, and high by the full board.
        self.observation_space = spaces.Box(low=self.board.empty_row, high=self.board.full_row, 
                                            shape=(self.get_state().shape), dtype=np.uint16)
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
        p = np.array([0 for i in range(self.max_piece_height)], np.uint16)
        for i in range(self.pieces[self.current_piece].orientations[0].height):
            p[i] = self.pieces[self.current_piece].orientations[0].shape[i]
        return np.concatenate((p, self.board.board), dtype=np.uint16)

    def render(self, mode='human'):
        print("Current piece:")
        print(self.pieces[self.current_piece])
        print(self.board)
    
    def close(self):
        pass

    def seed(self, seed_value: int):
        self.generator = np.random.default_rng(seed_value)

    def load_pieces(self, piece_file: str):
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

