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