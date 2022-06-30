from turtle import right
from torch import true_divide
from traitlets import Bool
import copy

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
    
    def show(self):
        self.block[19] = [1 for i in range(10)]
        for i in range(20):
            print(str(i).rjust(2), end=' ')
            for j in range(10):
                if self.block[i][j]:
                    print('■', end='')
                else:
                    print('□', end='')
            print()


class Block():
    def __init__(self, block_id:int, board:Board) -> None:
        self.block_id = block_id
        self.x, self.y = 3, -2
        self.status = 0
        self.block = [[0 for i in range(4)] for i in range(4)]
        self.board = board
        self.update()

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

    def fall(self) -> None:
        self.y += 1
        if(isCollision(self, self.board)):
            self.y -= 1
            return False
        else:
            return True
    
    def shiftRight(self) -> bool:
        rightLimit = 0
        for col in range(4):
            for row in range(4):
                if self.block[row][col] and col>rightLimit:
                    rightLimit = col

        if (self.x+rightLimit)==9:
            return False
        else:
            self.x += 1
            if(isCollision(self, self.board)):
                self.x -= 1
                return False
            else:
                return True

    def shiftLeft(self) -> bool:
        if (self.block_id == 6 and self.x == -1) or (self.block_id != 6 and self.x == 0):
            # 長條判斷條件是-1
            return False
        else:
            self.x -= 1
            if(isCollision(self, self.board)):
                self.x += 1                     # 修正
                return False
            else:
                return True

class TetrisGame():
    def __init__(self) -> None:
        

def view(block:Block, board:Board) -> list:
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
                views[onBoardY][onBoardX] = block.block[onBlockY][onBlockX]
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

board = Board()
# board.show()

block = Block(0, board)
# block.show()
# print()

views = view(block, board)


while 1:
    views = view(block, board)
    for i in range(20):
        print(str(i).rjust(2), end=' ')
        for j in range(10):
            if views[i][j]:
                print('■', end='')
            else:
                print('□', end='')
        print()
    action = input("Action: ")
    if action == 'd':
        block.fall()
    elif action == 'l':
        block.shiftLeft()
    elif action == 'r':
        block.shiftRight()
    elif action == 'f':
        block.rotate()
    else:
        continue    
