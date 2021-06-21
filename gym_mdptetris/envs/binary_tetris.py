
import gym
import os 
import random
import gym_mdptetris.envs.binary_piece as piece
import gym_mdptetris.envs.binary_board as board
import numpy as np

from gym import Env, spaces

class BinaryTetris():
    """
    A class which implements a standard game of Tetris for reinforcement learning
    conforming to the OpenAI Gym Env interface. 

    A board is instantiated and a piece set is loaded. The environment 
    implements a piece drop version of Tetris in contrast to the standard
    trajectory based implementation.

    Attribution: this environment is inspired by the MDPTetris environment
    of Scherrer and Thiery, http://mdptetris.gforge.inria.fr/doc/. 
    In addition method docstrings are adapted from OpenAI Gym source. 
    """

    def __init__(self, board_height=20, board_width=10, 
                piece_set='pieces4.dat', allow_overflow=False, seed=12345):
        """
        Constructor. Creates a board and setup for a gym environment. 
        reset() must be called before interacting with the environment.

        :param board_height: int, the height of the Tetris board.
        :param board_width: int, the width of the board.
        :param piece_set: str, path of the data file containing the pieces to be loaded.
        :param allow_overflow: bool, indicating if lines can overflow.
        :param seed: int, seed for random generator.

        TODO: Implement selected piece sequences
        """
        self.board_height = board_height
        self.board_width = board_width
        pieces_path = os.path.dirname(os.path.abspath(__file__)) + '/data/' + piece_set
        self.pieces, self.nb_pieces = self._load_pieces(pieces_path)
        self.max_piece_height = 0
        for piece in self.pieces:
            for o in piece.orientations:
                self.max_piece_height = max(self.max_piece_height, o.height)
        self.board = board.BinaryBoard(max_piece_height=self.max_piece_height, 
                width=board_width, height=board_height, allow_lines_after_overflow=allow_overflow)
        self.current_piece = 0
        random.seed(seed)
        # Observation is the representation of the current piece, concatenated with the board
        # TODO: restore observation space 
        self.observation_space = spaces.Tuple([spaces.Discrete(self.nb_pieces), 
            spaces.MultiBinary([self.board_height, self.board_width])])
        #self.observation_space = spaces.Box(low=False, high=True, 
        #                                    shape=(self.board_height, self.board_width), dtype='bool')

        # Action space is the board width multiplied by the max number of piece orientations, 
        # zero indexed (so less 1). 
        self.action_space = spaces.MultiDiscrete([4, self.board.width])

    def clamp(self, val, min, max):
        if val < min:
            return min
        elif val > max:
            return max
        else:
            return val

    def new_piece(self):
        # This delivers a dramatic improvement on speed
        self.current_piece = random.choice(range(self.nb_pieces))

    def step(self, action):
        """
        Run one step of the environment. 

        :param action: the piece drop action in the environment. Action // 10
            selects the orientation of the piece from 0-3, action % 10 selects
            the column placement, clipped to prevent the piece from exceeding
            the board width.
        :return:
            state: observation of the new state of the environment
            reward: reward of the action
            done: whether the episode has ended. After done is returned True
                further step() calls are undefined
            info: auxiliary information 
        """
        done = False
        orientation = self.clamp(action[0], 0, self.pieces[self.current_piece].nb_orientations - 1)
        column = self.clamp(action[1], 0, self.board_width - self.pieces[self.current_piece].orientations[orientation].width)
        reward = self.board.drop_piece(self.pieces[self.current_piece].orientations[orientation], column)
        if self.board.wall_height > self.board.height:
            done = True
        
        self.new_piece()
        return self._get_state(), reward, done, {}
    
    def reset(self):
        """
        Reset the environment board and select a new random piece. 

        :return: returns the current state
        """
        self.board.reset()
        #self.current_piece = self.generator.choice(self.nb_pieces)
        self.new_piece()
        return self._get_state()

    def _get_state(self):
        """
        Returns the current state of the environment as 1D numpy array.
        The state is represented by a concatenation of the current piece id
        and the board state. The board state is the underlying 1D numpy 
        integer array. For more details see the `Board` class. 
        """
        return (self.current_piece, self.board.board)

    def render(self, mode='human'):
        print("Current piece:")
        print(self.pieces[self.current_piece])
        print(self.board)
    
    def close(self):
        pass

    def seed(self, seed_value: int):
        """
        Alter the seed of the environment.

        :param seed_value: new seed value.
        """
        random.seed(seed_value)

    def _load_pieces(self, piece_file: str):
        """
        Load pieces from a data file. Comments in a file are marked by starting
        the line with '#'. The first non-comment line indicates the number
        of pieces in the file. Following non-comment lines identify pieces 
        by their number of orientations, height, and width, then describe
        their shape with a multiline string where 'X' represents a block and 
        ' ' an empty space. See data/ for examples. 

        TODO: Change parsing of pieces to more robust data format, JSON? 

        :param piece_file: path to data file containing pieces.
        """
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
            pieces.append(piece.BinaryPiece(nb_orientations, height, width, shape))
            curr_line += 1 + height 

        return pieces, nb_pieces

