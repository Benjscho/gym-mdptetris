import numpy as np
from brick_masks import brick_masks, brick_masks_inv

class PieceOrientation():
    def __init__(self, width, height, shape, nb_full_cells_on_rows):
        self.width = width
        self.height = height
        self.shape = shape
        self.nb_full_cells_on_rows = nb_full_cells_on_rows

    def __str__(self):
        s = ""
        for i in range(self.height):
            for j in range(self.width):
                if self.shape[i] & brick_masks[j]:
                    s += "X"
                else:
                    s += " "
            s += "\n"
        return s

class Piece():
    def __init__(self, nb_orientations, height, width, shape):
        self.nb_orientations = nb_orientations
        self.orientations = []
        piece = np.array([0]*height, np.uint16)
        nb_full_cells_on_rows = [0]*height
        i, j = 0, 0
        for c in shape.strip("\n"):
            if c == "X":
                piece[i] |= brick_masks[j]
                nb_full_cells_on_rows[i] += 1
                j += 1
            elif c == "\n":
                i += 1
                j = 0
            else:
                j += 1
        self.orientations.append(PieceOrientation(width, height, piece, nb_full_cells_on_rows))
        for o in range(1, nb_orientations):
            tmp = height
            height = width
            width = tmp 
            piece = np.array([0]*height, np.uint16)
            nb_full_cells_on_rows = [0]*height
            for i in range(height):
                for j in range(width):
                    if self.orientations[o-1].shape[width - 1 - j] & brick_masks[i]:
                        piece[i] |= brick_masks[j]
                        nb_full_cells_on_rows[i] += 1
            self.orientations.append(PieceOrientation(width, height, piece, nb_full_cells_on_rows))
    
    def __str__(self):
        return self.orientations[0].__str__()


