import numpy as np

cdef class CyBoard():
    cdef public: 
        int width
        int height
        bint allow_lines_after_overflow
        unsigned short full_row 
        unsigned short empty_row
        int extended_height
        int max_piece_height
        int wall_height
    
    def __init__(self, int max_piece_height=4, int width=10, int height=20, 
                bint allow_lines_after_overflow=False):
        self.width = width
        self.height = height
        self.allow_lines_after_overflow = allow_lines_after_overflow
        
        self.full_row = True
        self.empty_row = False

        self.max_piece_height = max_piece_height
        
        self.extended_height = height + self.max_piece_height

        self.board = np.zeros((self.extended_height, self.width), dtype='bool')
        self.wall_height = 0 
    
    def highest_block(self, arr, axis=0, invalid_val=-1):
        """
        Find the highest block in an array. Adapted from attribution code 
        Attribution: https://stackoverflow.com/a/47269413/14354978
        """
        mask = arr != False
        val = arr.shape[0] - np.flip(mask, axis=axis).argmax(axis=0) - 1
        return np.where(mask.any(axis=axis), val, -1)

    def lowest_block(self, arr, axis=0, invalid_val=-1):
        """
        Find the lowest block in an array. Used to find piece intersection.
        Adapted from attribution code 
        Attribution: https://stackoverflow.com/a/47269413/14354978
        """
        mask = arr != False 
        return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)

    cpdef drop_piece(self, oriented_piece, column: int, cancellable: bool = False):
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
            self.backup_board = np.copy(self.board)
            self.previous_wall_height = self.wall_height

        cdef int piece_height = oriented_piece.height
        cdef int piece_width = oriented_piece.width
        cdef int destination = -1
        cdef int removed_lines = 0 
        
        col_heights = self.highest_block(self.board[:, column:column+piece_width])
        piece_heights = self.lowest_block(oriented_piece.shape)

        cdef int i 
        cdef int intersect
        for i in range(piece_width):
            intersect = col_heights[i] - piece_heights[i]
            destination = np.maximum(destination, intersect)
        
        destination += 1

        cdef int j
        for i in range(destination, destination + piece_height):
            for j in range(column, column + piece_width):
                self.board[i][j] |= oriented_piece.shape[i - destination][j - column]

        cdef int destination_top = destination + piece_height
        cdef int wall_height = np.maximum(self.wall_height, destination_top)

        if destination_top <= self.height or self.allow_lines_after_overflow:
            i = 0
            i_stop = piece_height

            while i < i_stop:
                current_row = destination + i
                if np.all(self.board[current_row]) == True:
                    j = current_row
                    while j < wall_height -1 and np.all(self.board[j] != False):
                        self.board[j] = self.board[j+1]
                        j += 1
                    self.board[j] = False
                    wall_height -= 1
                    removed_lines += 1
                    i_stop -= 1 
                else:
                    i += 1
        self.wall_height = wall_height
        return removed_lines
    
    cpdef void reset(self):
        """
        Reset the state of the board.
        """        
        self.board = np.zeros((self.extended_height, self.width), dtype='bool')
        self.wall_height = 0
    
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
            self.backup_board = np.copy(self.board)
            self.previous_wall_height = self.wall_height

        cdef int piece_height = oriented_piece.height
        cdef int piece_width = oriented_piece.width
        cdef int destination = -1
        cdef int removed_lines = 0 

        col_heights = self.highest_block(self.board)
        piece_heights = self.lowest_block(oriented_piece.shape)
        cdef int i
        cdef int intersect
        for i in range(piece_width):
            intersect = col_heights[column + i] - piece_heights[i]
            destination = max(destination, intersect)
        destination += 1

        cdef int j 
        for i in range(destination, destination + piece_height):
            for j in range(column, column + piece_width):
                self.board[i][j] |= oriented_piece.shape[i - destination][j - column]

        cdef int destination_top = destination + piece_height
        cdef int wall_height = max(self.wall_height, destination_top)

        if destination_top <= self.height or self.allow_lines_after_overflow:
            i = 0
            i_stop = piece_height

            while i < i_stop:
                current_row = destination + i
                if np.all(self.board[current_row]) == True:
                    j = current_row
                    while j < wall_height -1 and np.all(self.board[j] != False):
                        self.board[j] = self.board[j+1]
                        j += 1
                    self.board[j] = False
                    wall_height -= 1
                    removed_lines += 1
                    i_stop -= 1
                else:
                    i += 1
        cdef int nb_over = 0
        if wall_height > self.height:
            nb_over = wall_height - self.height 
            self.board[:self.height] = self.board[nb_over:wall_height]
            self.board[self.height:] = False
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
            for j in range(self.width):
                if self.board[i][j]:
                    s += "X"
                else:
                    s += " "
            s += "\n"
        
        for i in range(self.height - 1, -1, -1):
            s += "|"
            for j in range(self.width):
                if self.board[i][j]:
                    s += "X"
                else:
                    s += "."
            s += "|\n"
        return s

class Board(CyBoard):
    def __init__(self, max_piece_height=4, width=10, height=20, 
                allow_lines_after_overflow=False):
        super(Board, self).__init__(max_piece_height=max_piece_height, 
                width=width, height=height, 
                allow_lines_after_overflow=allow_lines_after_overflow)
    