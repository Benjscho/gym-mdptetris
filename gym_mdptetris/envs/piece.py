import numpy as np
from brick_masks import brick_masks, brick_masks_inv

class PieceOrientation():
    def __init__(self, width: int, height: int, shape: np.ndarray, nb_full_cells_on_rows: list[int]):
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

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height and self.shape == other.shape

class Piece():
    def __init__(self, nb_orientations: int, height: int, width: int, shape: str):
        if nb_orientations < 1 or nb_orientations > 4:
            raise ValueError("Number of orientations must be between 1 and 4")
        if height <= 0:
            raise ValueError("Height must be positive integer")
        if width <= 0:
            raise ValueError("Width must be positive integer")
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
    
    def __eq__(self, other):
        if self.nb_orientations != other.nb_orientations:
            return False
        for i in range(self.nb_orientations):
            if self.orientations[i] != other.orientations[i]:
                return False
        return True


