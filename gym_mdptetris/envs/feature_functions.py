import numpy as np
import gym_mdptetris.envs.board as board

def get_landing_height(board: board.Board) -> float:
    """
    Feature 1 from the Dellacherie set. Returns the height the last
    piece was placed considering the middle of the piece.

    :param board: The current board state
    :return: 
    """
    if 'landing_height_center' in board.last_move_info:
        return board.last_move_info['landing_height_center']
    else:
        return 0

def get_eroded_cells(board: board.Board) -> float:
    if 'removed_lines' in board.last_move_info:
        return board.last_move_info['removed_lines'] * board.last_move_info['eliminated_bricks_in_last_piece']
    else:
        return 0

def get_row_transitions(board: board.Board) -> float:
    """
    Gets the number of row transitions on the board. 

    Side walls are considered full cells, so empty rows have two transitions.
    """
    temp = np.ones((board.height, board.width + 2), dtype='bool')
    temp[:, 1:-1] = board.board[:board.height,]
    return np.diff(temp).sum()

def get_col_transitions(board: board.Board) -> float:
    """
    Get number of column transitions on the board.

    The board floor is considered a full cell, so an empty column has 
    one transition. 
    """
    temp = np.ones((board.height + 1, board.width), dtype='bool')
    temp[1:,:] = board.board[:board.height,]
    return np.diff(temp.T).sum()

def get_holes(board: board.Board) -> float:
    pass