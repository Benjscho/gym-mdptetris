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