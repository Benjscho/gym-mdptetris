import os
import random
import numpy as np
import gym_mdptetris.envs.board as board
import gym_mdptetris.envs.piece as piece
import gym_mdptetris.envs.feature_functions as feature_funcs

class LinearGame():
    def __init__(self, weights: np.ndarray, board_height=20, board_width=10,  piece_set='pieces4.dat', seed=12345):
        self.weights = np.array([-1, 1, -1, -1, -4, -1], dtype='double')
        self.board_height = board_height
        self.board_width = board_width
        pieces_path = os.path.dirname(os.path.abspath(__file__)) + '/data/' + piece_set
        self.pieces, self.nb_pieces = piece.load_pieces(pieces_path)
        for p in self.pieces:
            for o in p.orientations:
                self.max_piece_height = max(self.max_piece_height, o.height)
        random.seed(seed)
        self.new_piece()
        self.board = board.Board(max_piece_height=self.max_piece_height,
            width=board_width, height=board_height)

    def get_dellacherie_features(self) -> np.ndarray:
        res = np.empty((6), dtype='double')
        for i, f in enumerate(feature_funcs.get_dellacherie_funcs()):
            res[i] = f(self.board)
        return res 
    
    def new_piece(self):
        self.current_piece = random.choice(range(self.nb_pieces))

    def board_step(self):
        actions = np.full((4, self.board_width), -np.inf, dtype='double')
        for i in range(self.pieces[self.current_piece].nb_orientations):
            for j in range(self.board_width - self.pieces[self.current_piece].orientations[i].width):
                self.board.drop_piece(self.pieces[self.current_piece].orientations[i],
                    column=j, cancellable=True)
                actions[i,j] = (self.get_dellacherie_features() * self.weights).sum()
                self.board.cancel_last_move()
        a = np.unravel_index(np.argmax(actions), actions.shape)
        return self.board.drop_piece(self.pieces[self.current_piece].orientations[a[0]], a[1])