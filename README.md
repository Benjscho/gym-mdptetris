# gym-mdptetris

gym-mdptetris provides reinforcement learning environments for Tetris based
upon a piece drop implementation of the game. Each transition moves from a 
state with a piece and a board state to a board state with the dropped piece
and a new piece. 

## Installation

gym-mdptetris is installable via github:
```bash
pip install git+https://github.com/Benjscho/gym-mdptetris
```

## State and Action Space
The state space is discrete and is given by an array 


## Coverage tests

First ensure you have `coverage` installed: `pip install coverage`.
To check code coverage the project needs to be built with the arg `coverage`.
For example, download the package and `cd` into its directory. It can then
be built and test coverage checked with the following commands:

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