import numpy as np 

class BinaryPieceOrientation():
    """
    Class defining an oriented piece. Pieces are represented as 1D arrays of
    integers. 
    """
    def __init__(self, width: int, height: int, shape, nb_full_cells_on_rows):
        """
        Constructor. Initiate a piece orientation.

        :param width: width of the piece orientation.
        :param height: height of the piece orientation
        :param shape: representation of the piece orientation as a 1D numpy
            integer array. 
        """
        self.width = width
        self.height = height
        self.shape = shape
        self.nb_full_cells_on_rows = nb_full_cells_on_rows

    def __str__(self):
        s = ""
        for i in range(self.height -1, -1, -1):
            for j in range(self.width):
                if self.shape[i][j] == True:
                    s += "X"
                else:
                    s += " "
            s += "\n"
        return s

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height and self.shape == other.shape

class BinaryPiece():
    """ 
    Class defining a piece as an array of PieceOrientations. 
    """
    def __init__(self, nb_orientations: int, height: int, width: int, shape: str):
        """
        Constructor. Takes in an initial orientation representation of a piece
        and initialises all of its orientations as an array of 
        PieceOrientations.

        :param nb_orientations: number of orientations this piece has
            based on 90 degree rotation.
        :param height: height of the initial orientation given in `shape`.
        :param width: width of the initial orientation given in `shape`.
        :param shape: string representation of the piece shape in its initial 
            orientation. 'X' indicates a full block, ' ' a space, and '\\n' 
            a newline. E.g., "XX\nXX" would represent the square Tetris block.
        """
        if nb_orientations < 1 or nb_orientations > 4:
            raise ValueError("Number of orientations must be between 1 and 4")
        if height <= 0:
            raise ValueError("Height must be positive integer")
        if width <= 0:
            raise ValueError("Width must be positive integer")
        if type(shape) != str: 
            raise TypeError("Shape must be a string")
        if "X" not in shape:
            raise ValueError("Shape cannot be empty")
        self.nb_orientations = nb_orientations
        self.orientations = []
        piece = np.zeros((height, width), dtype='bool')
        nb_full_cells_on_rows = [0]*height
        i, j = 0, 0
        for c in shape.strip("\n"):
            if c == "X":
                piece[i][j] = True
                nb_full_cells_on_rows[i] += 1
                j += 1
            elif c == "\n":
                i += 1
                j = 0
            else:
                j += 1
        self.orientations.append(BinaryPieceOrientation(width, height, piece, nb_full_cells_on_rows))
        for o in range(1, nb_orientations):
            tmp = height
            height = width
            width = tmp 
            piece = np.zeros((height, width), dtype='bool')
            nb_full_cells_on_rows = [0]*height
            for i in range(height):
                for j in range(width):
                    if self.orientations[o-1].shape[width - 1 - j][i] == True:
                        piece[i][j] = True
                        nb_full_cells_on_rows[i] += 1
            self.orientations.append(BinaryPieceOrientation(width, height, piece, nb_full_cells_on_rows))
    
    def __str__(self):
        return self.orientations[0].__str__()
    
    def __eq__(self, other):
        if self.nb_orientations != other.nb_orientations:
            return False
        for i in range(self.nb_orientations):
            if self.orientations[i] != other.orientations[i]:
                return False
        return True