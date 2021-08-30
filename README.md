# gym-mdptetris

gym-mdptetris provides reinforcement learning environments for Tetris based
upon a piece drop implementation of the game. Each transition moves from a 
state with a piece and a board state to a board state with the dropped piece
and a new piece. 

## Getting started
### Installation

gym-mdptetris is installable via github:
```bash
pip install git+https://github.com/Benjscho/gym-mdptetris
```
### Using the environments
To initialise an environment you can use the gym system:
```python
>>> import gym
>>> env = gym.make('gym_mdptetris:mdptetris-v0')
```

Or you can import the environment file directly:
```python
>>> import gym_mdptetris.envs.tetris as tetris
>>> env = tetris.Tetris()
```

When imported directly you can also customize the board size:
```python
>>> env = tetris.Tetris(board_height = 10, board_width = 10)
```

To customise the piece set used, create a piece data file in line with the
examples provided in `gym_mdptetris/envs/data` and save it to the same
directory. This file can then be input as a parameter to an environment
initialisation:
```python
>>> env = tetris.Tetris(piece_set = 'pieces3.dat')
```

### Environment listing

There are currently four environments provided as standard: 
- `mdptetris-v0`: The standard 20 x 10 Tetris game, with the observation returned as a two dimensional, (24, 10) Numpy ndarray of booleans.
- `mdptetris-v1`: The standard 20 x 10 Tetris game except with the state returned as a flattened array. 
- `melaxtetris-v0`: An implementation of the [Melax version of
    Tetris](https://melax.github.io/tetris/tetris.html), played on a 6 x 2 board,
    with the five pieces of between 1 x 1 and 2 x 2 size. In this version
    overflowing the board does not end the game, instead the lower lines are
    removed, the top lines moved down, and the step function returns the number of
    lines overflowed. 
- `melaxtetris-v1`: This is the same as the other Melax implementation, except
    the state array is flattened before being returned. 


### State and Action Space
The state space is discrete and is given by a Numpy boolean array of the board
with the piece shape arranged in additional rows above the board. The board size
is set by the board width, and the board height, with extra rows equal to the
maximum height of the pieces used.  In the flat environments the state array is
flattened prior to being returned. 

The action space is given as a tuple of `(o, c)`, where `o` is the orientation
index of the piece being dropped, and `c` is the column where it is to be 
dropped. Each piece has either 1, 2, or 4 orientations. If the values given
are outside of the possible range for orientations it is clipped (larger 
values are clipped to the max rotation, lower values are clipped to the 
first orientation). Similarly if the column placement of a piece would exceed
the bounds of the board, it is clipped to be within the board bounds. 

A raw state array of a game looks like this:
```python
>>> env._get_state()
array([[False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False, False, False, False, False, False, False, False, False, False],
       [False,  True, False, False, False, False, False, False, False, False],
       [ True,  True, False, False, False, False, False, False, False, False],
       [ True, False, False, False, False, False, False, False, False, False]])
```
The array has the shape (24, 10) as the board has an additional 4 rows to
contain the additional height of the pieces. You can see the current piece shape
in the last four rows, in this case the Z piece.


### Interacting with the environment

The game state can be shown in a human readable format by calling render, 
displaying the current piece, and the board state. 
```python
>>> env.render()
Current piece:
X 
X
X
X

|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
```

You can then make an action using the `step` function, with a tuple of piece
orientation and column placement. This will return a tuple of the observation,
the reward, an indication of if the new state is terminal, and an information
dictionary (currently unused).

```python
>>> env.step((0,0))
...
>>> env.render()
Current piece:
X 
XX
 X

|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|..........|
|X.........|
|X.........|
|X.........|
|X.........|
```

Here we have placed the piece in its 0th orientation, into the 0th column. 
Once the board overflows and a step returns a `done` value of True, 
subsequent behaviour is undefined, including rendering the game state. 

## Development

### Building

To (re)build the local files when developing you can `cd` to the root of the
project, and run `python setup.py build_ext --inplace`. This will build all of
the output and object files from the `.pyx` Cython code. If you have made
changes to a Cython file, you must rebuild the project before you can test them.

### Coverage tests

To run test coverage tests first ensure you have `coverage` installed: `pip
install coverage`.  To check code coverage the project needs to be built with
the `coverage` argument to set the linetrace visibility for Cython files.  For
example, download the package and `cd` into its directory. It can then be built
and test coverage checked with the following commands:

```bash
# Clean the build if you have already built or installed it
python setup.py cleanall

# Run setup with the coverage option
python setup.py coverage build_ext --inplace 

# Discover and run all tests
coverage run -m unittest discover

# Show coverage
coverage report
```

### Module Structure

The project is structured around a class structure which separates functionality
between the board, piece, and tetris files respectively. The board class manages
the state of the board, and piece placements. The piece class defines importing
pieces from the piece data files found in `gym_mdptetris/envs/data`. The tetris
file and classes therein manage tying the use of these classes together to 
form the environment loop. 