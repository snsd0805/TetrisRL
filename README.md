# TetrisRL
- Implement a reinforcement learning model which can play Tetris

# Tetris Enviroment
- 10 actions
    - 0: don't move
    - 1: shift left 1 block
    - 2: shift left 2 block
    - 3: shift left 3 block
    - 4: shift right 1 block
    - 5: shift right 2 block
    - 6: shift right 3 block
    - 7: rotate once
    - 8: rotate twice
    - 9: rotate three times
- return
    - pixel(10*20)
    - block_id
    - block_location(x, y)

# Version 0
- Policy Gradient Algorithm
- Reward Delay
- Bad Performance

# TODO
- change reward function
- reward baseline
- DQN