from game import TetrisGame

class TetrisEnviroment():
    def __init__(self) -> None:
        self.game = TetrisGame()
        self.score = 0
    
    def reset(self):
        self.game.reset()
        self.score = 0
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

        self.game.action('d')

        deltaScore = self.game.score - self.score
        self.score = self.game.score

        return self.game.view(), deltaScore, self.game.done, \
            (self.game.block.x, self.game.block.y, self.game.block.block_id) 
        # observation, reward, done, info(block location)