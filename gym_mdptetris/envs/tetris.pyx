import gym
import os 
import random
import gym_mdptetris.envs.piece as piece
import gym_mdptetris.envs.board as board
import gym_mdptetris.envs.feature_functions as ff
import numpy as np
cimport numpy as np

from gym import Env, spaces

cdef class CyTetris():
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

    cdef public:
        int nb_pieces
        int max_piece_height
        int current_piece
        int board_width
        int board_height

    def __init__(self, board_height=20, board_width=10, 
                piece_set='pieces4.dat', allow_overflow=False, seed=12345,
                flat_env=False):
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
        self.pieces, self.nb_pieces = piece.load_pieces(pieces_path)
        self.max_piece_height = 0
        self.flat_env = flat_env
        for p in self.pieces:
            for o in p.orientations:
                self.max_piece_height = max(self.max_piece_height, o.height)
        self.board = board.Board(max_piece_height=self.max_piece_height, 
                width=board_width, height=board_height, allow_lines_after_overflow=allow_overflow)
        self.current_piece = 0

        random.seed(seed)
        self.observation_space = self.get_observation_space()

        self.action_space = spaces.MultiDiscrete([4, self.board.width])

    cdef clamp(self, int val, int min, int max):
        if val < min:
            return min
        elif val > max:
            return max
        else:
            return val

    cdef void new_piece(self):
        # This delivers a dramatic improvement on speed
        self.current_piece = random.choice(range(self.nb_pieces))

    cpdef step(self, action):
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
        cdef int orientation
        cdef int column
        cdef bint done = False
        orientation = self.clamp(action[0], 0, self.pieces[self.current_piece].nb_orientations - 1)
        column = self.clamp(action[1], 0, self.board_width - self.pieces[self.current_piece].orientations[orientation].width)
        reward = self.board.drop_piece(self.pieces[self.current_piece].orientations[orientation], column)
        if self.board.wall_height > self.board.height:
            done = True
        self.new_piece()
        return self._get_state(), reward, done, {}

    cpdef get_dellacherie_state(self):
        cdef np.ndarray res 
        cdef int i 
        res = np.empty((6), dtype='double')
        for i, f in enumerate(ff.get_dellacherie_funcs()):
            res[i] = f(self.board)
        return res 
    
    cpdef reset(self):
        """
        Reset the environment board and select a new random piece. 

        :return: returns the current state
        """
        self.board.reset()
        self.new_piece()
        return self._get_state()

    def get_observation_space(self):
        spaces.MultiBinary([self.board.extended_height, self.board_width])

    cpdef _get_state(self):
        """
        Returns the current state of the environment as 1D numpy array.
        The state is represented by a concatenation of the current piece id
        and the board state. The board state is the underlying 1D numpy 
        integer array. For more details see the `Board` class. 
        """
        temp = np.copy(self.board.board)
        temp[-4:, :] = False
        temp[-self.pieces[self.current_piece].orientations[0].height:,:self.pieces[self.current_piece].orientations[0].width] = self.pieces[self.current_piece].orientations[0].shape
        if self.flat_env:
            return temp.flatten()
        else:
            return temp

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
    

class Tetris(CyTetris, Env):
    """
    A class which implements a standard game of Tetris for reinforcement learning
    conforming to the OpenAI Gym Env interface. Extends the Cython Extension
    Type to enable direct Python access. 

    A board is instantiated and a piece set is loaded. The environment 
    implements a piece drop version of Tetris in contrast to the standard
    trajectory based implementation.

    Attribution: this environment is inspired by the MDPTetris environment
    of Scherrer and Thiery, http://mdptetris.gforge.inria.fr/doc/. 
    In addition method docstrings are adapted from OpenAI Gym source. 

    :param board_height: int, the height of the Tetris board.
    :param board_width: int, the width of the board.
    :param piece_set: str, path of the data file containing the pieces to be loaded.
    :param allow_overflow: bool, indicating if lines can overflow.
    :param seed: int, seed for random generator.
    """
    def __init__(self, board_height=20, board_width=10, piece_set='pieces4.dat', 
                allow_overflow=False, seed=12345, flat_env=False):
        """
        Constructor. Creates a board and setup for a gym environment. 
        reset() must be called before interacting with the environment.
        """
        super(Tetris, self).__init__(board_height=board_height, board_width=board_width,
                piece_set=piece_set, allow_overflow=allow_overflow, seed=seed, 
                flat_env=flat_env)

class TetrisFlat(Tetris):
    def __init__(self):
        super(TetrisFlat, self).__init__(flat_env=True)

    def get_observation_space(self):
        return spaces.MultiBinary(self.board.extended_height * self.board_width)

class TetrisHeuristic(Tetris):
    def __init__(self):
        super(TetrisHeuristic, self).__init__()

    def _get_state(self):
        return self.get_dellacherie_state()

    def get_observation_space(self):
        return spaces.Box(low=-100, high=100, shape=(6,), dtype=np.float)

cdef class CyMelaxTetris(CyTetris):
    """
    A class which implements a reduced board size game of Tetris for reinforcement learning.
    """
    cdef public:
        int max_pieces
        int piece_drops

    def __init__(self, max_pieces=1000, flat_env=True):
        super(CyMelaxTetris, self).__init__(board_height=2, board_width=6, 
                piece_set='pieces_melax.dat', allow_overflow=True, flat_env=flat_env)
        self.piece_drops = 0
        self.max_pieces = max_pieces

    def step(self, action):
        self.piece_drops += 1
        cdef bint done = False
        orientation = self.clamp(action[0], 0, self.pieces[self.current_piece].nb_orientations - 1)
        column = self.clamp(action[1], 0, self.board_width - self.pieces[self.current_piece].orientations[orientation].width)
        reward = -self.board.drop_piece_overflow(self.pieces[self.current_piece].orientations[orientation], column)
        if self.piece_drops > self.max_pieces:
            done = True
        self.new_piece()
        return self._get_state(), reward, done, {}
       
    def reset(self):
        self.board.reset()
        self.new_piece()
        self.piece_drops = 0
        return self._get_state()

class MelaxTetris(CyMelaxTetris, Env):
    def __init__(self, max_pieces=1000, flat_env=False):
        super(MelaxTetris, self).__init__(max_pieces=max_pieces, flat_env=flat_env)

class MelaxTetrisFlat(MelaxTetris):
    def __init__(self):
        super(MelaxTetrisFlat, self).__init__(flat_env=True)

    def get_observation_space(self):
        return spaces.MultiBinary(self.board.extended_height * self.board_width)

class MelaxTetrisHeuristic(MelaxTetris):
    def __init__(self):
        super(MelaxTetrisHeuristic, self).__init__()

    def _get_state(self):
        return self.get_dellacherie_state()

    def get_observation_space(self):
        return spaces.Box(low=-100, high=100, shape=(6,), dtype=np.float)