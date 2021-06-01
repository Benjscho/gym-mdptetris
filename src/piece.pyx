cdef struct PieceOrientation:
    int width
    int height
    unsigned short *bricks
    int *nb_full_cells_on_rows

cdef struct Piece:
    int nb_orientations
    PieceOrientation *orientations 

cdef void load_pieces(str file_name, int nb_pieces, Piece **pieces):

    f = open(file_name, "r")
    if not f:
        raise ValueError("Could not real the pieces file: {file_name}")
    
    lines = f.readlines()
    i = 0
    while nb_pieces == 0:
        if lines[i][0] == '#':
            i += 1
            continue
        nb_pieces = int(lines[i])
        i += 1
    
    for j in range(nb_pieces):
        if lines[i][0] == '#':
            i += 1
            continue
        