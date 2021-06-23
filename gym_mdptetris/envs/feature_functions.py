import numpy as np
import gym_mdptetris.envs.board as board

def get_landing_height(board: board.Board) -> float:
    """
    Feature 1 from the Dellacherie set. Returns the height the last
    piece was placed considering the middle of the piece.

    :param board: The current board state
    :return: Landing height of the previous piece 
    """
    if 'landing_height_center' in board.last_move_info:
        return board.last_move_info['landing_height_center']
    else:
        return 0

def get_eroded_cells(board: board.Board) -> float:
    """
    Feature 2 from the Dellacherie set. Returns the product of removed lines
    and the number of bricks from the last piece in those lines.

    :param board: The current board state
    :return: Number of eroded cells 
    """
    if 'removed_lines' in board.last_move_info:
        return board.last_move_info['removed_lines'] * board.last_move_info['eliminated_bricks_in_last_piece']
    else:
        return 0

def get_row_transitions(board: board.Board) -> float:
    """
    Gets the number of row transitions on the board. 

    Side walls are considered full cells, so empty rows have two transitions.

    :param board: The current board state
    :return: Number of row transitions
    """
    temp = np.ones((board.height, board.width + 2), dtype='bool')
    temp[:, 1:-1] = board.board[:board.height,]
    return np.diff(temp).sum()

def get_col_transitions(board: board.Board) -> float:
    """
    Get number of column transitions on the board.

    The board floor is considered a full cell, so an empty column has 
    one transition. 

    :param board: The current board state
    :return: Number of column transitions 
    """
    temp = np.ones((board.height + 1, board.width), dtype='bool')
    temp[1:,:] = board.board[:board.height,]
    return np.diff(temp.T).sum()

def hole_helper(arr: np.ndarray):
    """
    Helper function that sums the False values in a row that precede
    at least one True value. 
    Attribution: https://stackoverflow.com/a/68087910/14354978
    """
    return np.max((~arr).cumsum(axis = 1) * arr, axis = 1).sum()

def get_holes(board: board.Board) -> float:
    return hole_helper(board.board.T)

def get_well_sums(board: board.Board) -> float:
    """
    A well cell is an empty cell where the left and right cell are both full,
    and the cell above it is empty.

    For example:
    |..........|
    |..........|
    |..........|
    |..........|
    |...X......|
    |...X.XX...|
    |..XX.X....|
    |XXXX.XXXXX|
    |X.X.XXX.X.|
    |X.X.XXX.X.|

    This board has 7 well cells as indicated below with 'o'

    |..........|
    |..........|
    |..........|
    |..........|
    |...X......|
    |...XoXX...|
    |..XXoX....|
    |XXXXoXXXXX|
    |X.X.XXX.X.|
    |XoXoXXXoXo|

    This is calculated using the `np.roll()` function to shift the array
    one column left, one column right, and one row down. The result of 
    these are then AND-ed with the complement of the cell to indicate
    if the cell is a well, before summing.

    To indicate that board walls count for wells extra columns are added either
    side, and a row of false is added at the bottom to indicate well cells 
    at the top row count. 

    :param board: The current board state
    :return: The sum total of well cells on the board.
    """
    temp = np.ones((board.height + 1, board.width + 2), dtype='bool')
    #temp[:,-1:] = False
    #temp[:,:1] = False
    temp[:1] = False
    temp[1:,1:-1] = board.board[:board.height,]
    return (np.roll(temp, 1, axis=1) & np.roll(temp, -1, axis=1) & ~temp & ~np.roll(temp, -1, axis=0)).sum()

def get_wall_height(board: board.Board) -> float:
    return board.wall_height

