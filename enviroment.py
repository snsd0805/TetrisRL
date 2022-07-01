from game import TetrisGame

class TetrisEnviroment():
    def __init__(self) -> None:
        self.game = TetrisGame()
        self.score = 0
        self.pastHeights = 0
        self.pastHoles = 0
    
    def reset(self):
        self.game.reset()
        self.score = 0
        self.pastHeights = 0
        self.pastHoles = 0

        return self.game.view(), 0, self.game.done, \
                (self.game.block.x, self.game.block.y, self.game.block.block_id) 
    
    def step(self, mode):
        if mode == 0:   # 不動
            None
        elif mode == 1: # left 1
            self.game.action('l')
        elif mode == 2: # left 2
            for i in range(2):
                self.game.action('l')
        elif mode == 3: # left 3
            for i in range(3):
                self.game.action('l')
        elif mode == 4: # right 1
            self.game.action('r')
        elif mode == 5: # right 2
            for i in range(2):
                self.game.action('r')
        elif mode == 6: # right 3
            for i in range(3):
                self.game.action('r')
        elif mode == 7: # rotate 1
            self.game.action('f')
        elif mode == 8: # rotate 2
            for i in range(2):
                self.game.action('f')
        elif mode == 9: # rotate 3
            for i in range(3):
                self.game.action('f')

        fallStatus = self.game.action('d')

        
        # 開始計算 rewards
        # 1. 消除 line
        completeLines = self.game.score - self.score
        self.score = self.game.score

        # 2. block 總高度
        heights = self.game.getAggregateHeight()

        # 3. hole 數量
        holes = self.game.getHoleNumber()

        # 根據權重計算 rewards
        # https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
        rewards = -0.5*(heights-self.pastHeights) + 2*completeLines + -0.3*(holes-self.pastHoles)
        if fallStatus == False:
            rewards += 1

        self.pastHeights = heights
        self.pastHoles = holes

        return self.game.view(), rewards, self.game.done, \
            (self.game.block.x, self.game.block.y, self.game.block.block_id, completeLines)
        # observation, reward, done, info(block location)


# env = TetrisEnviroment()
# pixel, reward, done, info = env.reset()
# while 1:
#     for i in range(20):
#         print(str(i).rjust(2), end=' ')
#         for j in range(10):
#             if pixel[i][j]:
#                 print('■', end='')
#             else:
#                 print('□', end='')
#         print()
#     action = int(input("Action: "))
#     pixel, reward, done, info = env.step(action)
#     print(pixel, reward, done, info)
#     print("Rewards: ", reward)
#     if done:
#         break
