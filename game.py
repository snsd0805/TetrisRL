import random

BLOCK_FILL_LOC = [
    [[9, 10, 12, 13], [4, 8, 9, 13]],
    [[8, 9, 13, 14], [5, 8, 9, 12]],
    [[8, 12, 13, 14], [4, 5, 8, 12], [8, 9, 10, 14], [5, 9, 12, 13]],
    [[10, 12, 13, 14], [4, 8, 12, 13], [8, 9, 10, 12], [4, 5, 9, 13]],
    [[9, 12, 13, 14], [4, 8, 9, 12], [8, 9, 10, 13], [5, 8, 9, 13]],
    [[8, 9, 12, 13]],
    [[12, 13, 14, 15], [1, 5, 9, 13]]
]


class Board():
    '''
    |
  --|-------------
  0 |     |----
    |     |
    |     |
    |
    |
 19 |
    '''
    def __init__(self) -> None:
        self.block = [[0 for _ in range(10)] for _ in range(20)]
        
    def place(self, block):
        '''
            把現在的方塊擺進去 board，代表確定方塊位置了
        '''
        self.block = view(self, block)
    
    def checkScore(self) -> int:
        '''
            檢查是否有連線，並回傳該動作得到的分數
        '''
        score = 0
        for row in range(20):
            flag = True
            for col in range(10):
                if self.block[row][col] == 0:
                    flag = False
                    break
            if flag:
                score += 1
                self.block[0] = [0 for i in range(10)]
                for updateRow in range(row, 0, -1):
                    self.block[updateRow] = self.block[updateRow-1]
        return score

class Block():
    def __init__(self, block_id:int, board:Board) -> None:
        self.block_id = block_id
        self.x, self.y = 3, -2
        self.status = 0
        self.block = [[0 for i in range(4)] for i in range(4)]
        self.board = board
        self.update()
    
    def reset(self):
        block_id = random.randint(0, 6)
        self.__init__(block_id, self.board)

    def update(self):
        id = self.block_id
        status = self.status

        block = [[0 for i in range(4)] for i in range(4)]
        counter = 0
        for i in range(4):
            for j in range(4):
                if counter in BLOCK_FILL_LOC[id][status]:
                    block[i][j] = 1
                counter += 1
        self.block = block
    
    def show(self) -> None:
        for i in range(4):
            for j in range(4):
                if self.block[i][j]:
                    print('■', end='')
                else:
                    print('□', end='')
            print()
    
    def rotate(self) -> None:
        self.status = (self.status+1)%len(BLOCK_FILL_LOC[self.block_id])
        self.update()
        if(isCollision(self, self.board)):
            self.status = (self.status-1)%len(BLOCK_FILL_LOC[self.block_id])
            self.update()
            return False
        else:
            return True

    def fall(self) -> bool:
        self.y += 1
        if(isCollision(self, self.board)):
            self.y -= 1
            self.board.place(self)
            self.reset()
            return False
        else:
            return True
    
    def shiftRight(self) -> bool:
        self.x += 1
        if(isCollision(self, self.board)):
            self.x -= 1
            return False
        else:
            return True

    def shiftLeft(self) -> bool:
        self.x -= 1
        if(isCollision(self, self.board)):
            self.x += 1                     # 修正
            return False
        else:
            return True

class TetrisGame():
    def __init__(self) -> None:
        block_id = random.randint(0, 6)
        self.board = Board()
        self.block = Block(block_id, self.board)

        self.score = 0
    
    def action(self, mode):
        if mode == 'd':
            self.block.fall()
        elif mode == 'l':
            self.block.shiftLeft()
        elif mode == 'r':
            self.block.shiftRight()
        elif mode == 'f':
            self.block.rotate()
        
        self.score += self.board.checkScore()
        print("SCORE:", self.score)
    
    def view(self):
        return view(self.board, self.block)

def view(board:Board, block:Block) -> list:
    views = []
    for row in board.block:
        views.append([])
        for col in row:
            views[-1].append(col)
    for onBlockY in range(4):
        onBoardY = block.y+onBlockY
        if onBoardY >= 0:
            for onBlockX in range(4):
                onBoardX = block.x+onBlockX
                if onBoardX >= 10:
                    break
                if block.block[onBlockY][onBlockX] == 1:
                    views[onBoardY][onBoardX] = 1
    return views

def isCollision(block:Block, board:Board) -> bool:
    for onBlockY in range(4):
        onBoardY = block.y+onBlockY
        for onBlockX in range(4):
            onBoardX = block.x+onBlockX
            if block.block[onBlockY][onBlockX]==1:
                if onBoardX >= 10 or onBoardX < 0 or onBoardY >= 20 or onBoardY < 0:
                    return True
                if board.block[onBoardY][onBoardX]==1:
                    return True
    return False