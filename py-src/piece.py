import numpy as np

brick_masks = np.array([
  0x8000, # X............... */
  0x4000, # .X.............. */
  0x2000, # ..X............. */
  0x1000, # etc */
  0x0800,
  0x0400,
  0x0200,
  0x0100,
  0x0080,
  0x0040,
  0x0020,
  0x0010,
  0x0008,
  0x0004,
  0x0002, # ..............X. */
  0x0001  # ...............X */
], np.uint16)

brick_masks_inv = np.array([
  0x7FFF, # .XXXXXXXXXXXXXXX */
  0x4000, # X.XXXXXXXXXXXXXX */
  0x2000, # XX.XXXXXXXXXXXXX */
  0x1000, # etc */
  0x0800,
  0x0400,
  0x0200,
  0x0100,
  0x0080,
  0x0040,
  0x0020,
  0x0010,
  0x0008,
  0x0004,
  0x0002, # XXXXXXXXXXXXXX.X */
  0x0001  # XXXXXXXXXXXXXXX. */
], np.uint16)

class Board():
    def __init__(self, width, height, nb_pieces, pieces)
        self.width = width
        self.height = height
        self.pieces = pieces
        
        self.full_row = 0xFFFF
        self.empty_row = brick_masks[0] | brick_masks[width+1]
        for i in range(width+2, 16):
            self.empty_row |= brick_masks[i]
        self.board = np.array([self.empty_row]*self.height], np.uint16)

        self.max_piece_height = 0
        for i in range(nb_pieces):
            for j in range(pieces[i].nb_orientations):
                self.max_piece_height = max(self.max_piece_height, pieces[i].orientations[j].height)

    def reset(self):
        self.board = np.array([self.empty_row]*self.height], np.uint16)
    
    def drop_piece(self, piece, action, cancellable):
        pass

    def cancel_last_move(self):
        pass

    def get_column_height(self, column):
        pass

    def print_board(self):
        pass