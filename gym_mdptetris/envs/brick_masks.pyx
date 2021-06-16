from cpython cimport array
"""
Brick masks used in identifying brick locations on the Tetris board.

Attribution: taken from the MDPTetris implementation by Scherrer and Theirry
(http://mdptetris.gforge.inria.fr/doc/). 
"""

cdef array.array brick_masks = array.array('H', [
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
])

cdef array.array brick_masks_inv = array.array('H', [
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
])
