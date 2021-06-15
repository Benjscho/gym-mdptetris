import numpy as np
from gym_mdptetris.envs.brick_masks import brick_masks, brick_masks_inv


class Board():
    """
    Board class. Implements a Tetris board as a 1D array of integers. Each
    row of the board is represented by a 16 bit integer
    """
    def __init__(self, max_piece_height=4, width=10, height=20, 
                allow_lines_after_overflow=False):
        """
        Constructor. Initialises an empty board. 

        :param max_piece_height: max height of any piece passed to the board.
        :param width: width of the board.
        :param height: height of the board.
        :param allow_lines_after_overflow: allow placement after exceeding
            board height. 
        """
        if width > 14 or width < 5: 
            raise ValueError(f"Width must be between 5 and 14, value given: {width}")
        if max_piece_height > height:
            raise ValueError(f"Max piece height exceeds board height, max_piece_height: {max_piece_height}")
        self.width = width
        self.height = height
        self.allow_lines_after_overflow = allow_lines_after_overflow
        
        self.full_row = 0xFFFF
        self.empty_row = brick_masks[0] | brick_masks[width+1]
        for i in range(width+2, 16):
            self.empty_row |= brick_masks[i]

        self.max_piece_height = max_piece_height
        
        self.extended_height = height + self.max_piece_height

        self.board = np.array([self.empty_row]*self.extended_height, np.int16)
        self.wall_height = 0


    def reset(self):
        """
        Reset the state of the board.
        """        
        self.board = np.array([self.empty_row]*self.extended_height, np.int16)
        self.wall_height = 0
    
    def drop_piece(self, oriented_piece, column: int, cancellable: bool = False):
        """
        Method to implement piece drop on a board. 

        :param oriented_piece: a PieceOrientation object to be dropped on
            the board.
        :param column: the column the piece should be dropped in. The column
            should be less than `board_width - oriented_piece.width` as there
            are no protections against piece overflow in this method due to
            speed requirements.
        :param cancellable: bool, backs up the board state if true. 
        :return:
            Returns the number of rows cleared by a piece drop for use as a 
            reward signal.
        """
        if cancellable:
            self.backup_board = self.board.copy()
            self.previous_wall_height = self.wall_height

        piece_height = oriented_piece.height
        destination = self.wall_height
        removed_lines = 0 

        collision = 0
        # Descend the piece while there has been no collision and while the 
        # piece is on the board.
        while destination >= 0 and not collision:
            current_row = destination
            i = 0 
            # Iterate through the piece height to detect collision
            while i < piece_height and not collision:
                collision = self.board[current_row] & (oriented_piece.shape[piece_height - i - 1] >> column)
                i += 1
                current_row += 1
            if not collision:
                destination -= 1
        destination += 1

        destination_top = destination + piece_height

        wall_height = np.maximum(self.wall_height, destination_top)

        for i in range(piece_height):
            self.board[destination + i] |= oriented_piece.shape[piece_height - i - 1] >> column

        if destination_top <= self.height or self.allow_lines_after_overflow:
            i = 0
            i_stop = piece_height

            while i < i_stop:
                current_row = destination + i
                if self.board[current_row] == self.full_row:
                    j = current_row
                    while j < wall_height -1 and self.board[j] != self.empty_row:
                        self.board[j] = self.board[j+1]
                        j += 1
                    self.board[j] = self.empty_row
                    wall_height -= 1
                    removed_lines += 1
                    i_stop -= 1
                else:
                    i += 1
        self.wall_height = wall_height
        return removed_lines

    def drop_piece_overflow(self, oriented_piece, column: int, cancellable: bool = False):
        """
        Method to implement piece drop on a board. If the board overflows as
        a result, remove rows from the bottom up until the board is within 
        bounds again. Used in small state space versions of Tetris, or 
        implementations that minimise row overflow. 

        :param oriented_piece: a PieceOrientation object to be dropped on
            the board.
        :param column: the column the piece should be dropped in. The column
            should be less than `board_width - oriented_piece.width` as there
            are no protections against piece overflow in this method due to
            speed requirements.
        :param cancellable: bool, backs up the board state if true. 
        :return:
            Returns the number of rows the last piece exceeded the height
            of the board by. Used as a reward signal. 
        """
        if cancellable:
            self.backup_board = self.board
            self.previous_wall_height = self.wall_height

        piece_height = oriented_piece.height
        destination = self.wall_height
        removed_lines = 0 

        collision = 0
        while destination >= 0 and not collision:
            current_row = destination
            i = 0 
            while i < piece_height and not collision:
                collision = self.board[current_row] & (oriented_piece.shape[piece_height - i - 1] >> column)
                i += 1
                current_row += 1
            if not collision:
                destination -= 1
        destination += 1

        destination_top = destination + piece_height

        wall_height = max(self.wall_height, destination_top)

        for i in range(piece_height):
            self.board[destination + i] |= oriented_piece.shape[piece_height - i - 1] >> column

        if destination_top <= self.height or self.allow_lines_after_overflow:
            i = 0
            i_stop = piece_height

            while i < i_stop:
                current_row = destination + i
                if self.board[current_row] == self.full_row:
                    j = current_row
                    while j < wall_height -1 and self.board[j] != self.empty_row:
                        self.board[j] = self.board[j+1]
                        j += 1
                    self.board[j] = self.empty_row
                    wall_height -= 1
                    removed_lines += 1
                    i_stop -= 1
                else:
                    i += 1
        nb_over = 0
        if wall_height > self.height:
            nb_over = wall_height - self.height 
            self.board[:self.height] = self.board[nb_over:wall_height]
            self.board[self.height:] = self.empty_row
            wall_height = self.height

        self.wall_height = wall_height
        return nb_over

    def cancel_last_move(self):
        """
        Uses board backup to cancel the last move. Used in linear evaluation.
        """
        self.board = self.backup_board
        self.wall_height = self.previous_wall_height
        
    def get_column_height(self, column):
        pass

    def __str__(self):
        """
        :return: returns board state as a printable string. 
        """
        s = ""
        for i in range(self.wall_height, self.height - 1, -1):
            s += " "
            for j in range(1, self.width +1):
                if self.board[i] & brick_masks[j]:
                    s += "X"
                else:
                    s += " "
            s += "\n"
        
        for i in range(self.height - 1, -1, -1):
            s += "|"
            for j in range(1, self.width+1):
                if self.board[i] & brick_masks[j]:
                    s += "X"
                else:
                    s += "."
            s += "|\n"
        return s