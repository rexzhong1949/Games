'''
Function:
    定义游戏精灵类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
from tarfile import RECORDSIZE
import pygame
import copy

'''定义hero'''
class Hero(pygame.sprite.Sprite):
    def __init__(self, image, coordinate, block_size, border_size, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (block_size, block_size))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate[0] * block_size + border_size[0], coordinate[1] * block_size + border_size[1]
        self.coordinate = coordinate
        self.block_size = block_size
        self.border_size = border_size
        self.path = [self.rect.center]

    def SmartMove(self, maze):
        #深度复制，避免修改影响原迷宫的数据    
        blocks_list = copy.deepcopy(maze.blocks_list)
        block_now = blocks_list[0][0]
        exit_block = blocks_list[-1][-1]
        records = []
        next_block = None
        while block_now!=exit_block:
            is_move = False
            print(block_now.coordinate)
            #按上下左右的顺序，按深度遍历
            if not block_now.has_walls[0]:      #up
                next_block = blocks_list[block_now.coordinate[0]][block_now.coordinate[1]-1]
                if next_block not in records:
                    records.append(block_now)
                    block_now = next_block
                    is_move = True
                    continue
            if not block_now.has_walls[1]:      #down
                next_block = blocks_list[block_now.coordinate[0]][block_now.coordinate[1]+1]
                if next_block not in records:
                    records.append(block_now)
                    block_now = next_block
                    is_move = True
                    continue
            if not block_now.has_walls[2]:      #left
                next_block = blocks_list[block_now.coordinate[0]-1][block_now.coordinate[1]]
                if next_block not in records:
                    records.append(block_now)
                    block_now = next_block
                    is_move = True
                    continue
            if not block_now.has_walls[3]:      #right
                next_block = blocks_list[block_now.coordinate[0]+1][block_now.coordinate[1]]
                if next_block not in records:
                    records.append(block_now)
                    block_now = next_block
                    is_move = True
                    continue

            if not is_move:
                block_now = records.pop()            

        records.append(block_now)
        return records


    '''移动'''
    def move(self, direction, maze):
        blocks_list = maze.blocks_list
        if direction == 'up':
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[0]:
                return False
            else:
                self.coordinate[1] = self.coordinate[1] - 1
                return True
        elif direction == 'down':
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[1]:
                return False
            else:
                self.coordinate[1] = self.coordinate[1] + 1
                return True
        elif direction == 'left':
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[2]:
                return False
            else:
                self.coordinate[0] = self.coordinate[0] - 1
                return True
        elif direction == 'right':
            if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[3]:
                return False
            else:
                self.coordinate[0] = self.coordinate[0] + 1
                return True
        else:
            raise ValueError('Unsupport direction %s in Hero.move...' % direction)
    '''绑定到屏幕'''
    def draw(self, screen):
        self.rect.left, self.rect.top = self.coordinate[0] * self.block_size + self.border_size[0], self.coordinate[1] * self.block_size + self.border_size[1]
        screen.blit(self.image, self.rect)