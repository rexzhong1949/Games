'''
Function:
    随机生成迷宫
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
import random
from .misc import showText, Button, Interface


'''一个游戏地图块'''
class Block():
    def __init__(self, coordinate, block_size, border_size, **kwargs):
        # (col, row)
        self.coordinate = coordinate
        self.block_size = block_size
        self.border_size = border_size
        self.is_visited = False
        # 上下左右有没有墙，一个块默认为4面都是墙，顺序是上下左右
        self.has_walls = [True, True, True, True]
        self.color = (0, 0, 0)
    '''画到屏幕上'''
    def draw(self, screen):
        directions = ['top', 'bottom', 'left', 'right']
        for idx, direction in enumerate(directions):
            if self.has_walls[idx]:
                if direction == 'top':
                    x1 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y1 = self.coordinate[1] * self.block_size + self.border_size[1]
                    x2 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y2 = self.coordinate[1] * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
                elif direction == 'bottom':
                    x1 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y1 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    x2 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y2 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
                elif direction == 'left':
                    x1 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y1 = self.coordinate[1] * self.block_size + self.border_size[1]
                    x2 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y2 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
                elif direction == 'right':
                    x1 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y1 = self.coordinate[1] * self.block_size + self.border_size[1]
                    x2 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y2 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
        return True


'''随机生成迷宫类'''
#原理可以搜索“使用prim算法生成随机迷宫”和“三大迷宫生成算法 (Maze generation algorithm) -- 深度优先，随机Prim，递归分割”
'''设迷宫入口为左上角的路径格，
出口为右下角的路径格，
则生成一个迷宫的实质就是找G的一个最小生成树T，
T包含所有路径格，不成环，且其中任意两个路径格连通。
满足这个条件，则从任意一个格子出发都能到达迷宫的出口，不存在死角。
如果只打通出入口之间的路线就退出，迷宫就太简单了'''
class RandomMaze():
    def __init__(self, maze_size, block_size, border_size,screen, **kwargs):
        self.block_size = block_size
        self.border_size = border_size
        self.maze_size = maze_size
        self.screen = screen
        self.blocks_list = RandomMaze.createMaze(maze_size, block_size, border_size,screen)
        self.font = pygame.font.SysFont('Consolas', 15)
    '''画到屏幕上'''
    def draw(self, screen):
        for row in range(self.maze_size[0]):
            for col in range(self.maze_size[1]):
                self.blocks_list[row][col].draw(screen)
        # 起点和终点标志
        showText(screen, self.font, 'S', (255, 0, 0), (self.border_size[0]-10, self.border_size[1]))
        showText(screen, self.font, 'D', (255, 0, 0), (self.border_size[0]+(self.maze_size[1]-1)*self.block_size, self.border_size[1]+self.maze_size[0]*self.block_size+5))
    '''创建迷宫'''
    #关键函数，看懂如何创建的迷宫，理解迷宫的数据结构
    @staticmethod
    def createMaze(maze_size, block_size, border_size,screen):
        #
        def nextBlock(block_now, blocks_list):
            directions = ['top', 'bottom', 'left', 'right']
            blocks_around = dict(zip(directions, [None]*4))
            '''blocks_around形如{'top': None, 'bottom': None, 'left': None, 'right': None}'''
            #print(blocks_around)
            block_next = None
            count = 0
            # 查看上边block，条件是判断不是最顶上的block
            if block_now.coordinate[1]-1 >= 0:
                block_now_top = blocks_list[block_now.coordinate[1]-1][block_now.coordinate[0]]
                if not block_now_top.is_visited:
                    blocks_around['top'] = block_now_top
                    count += 1
            # 查看下边block
            if block_now.coordinate[1]+1 < maze_size[0]:
                block_now_bottom = blocks_list[block_now.coordinate[1]+1][block_now.coordinate[0]]
                if not block_now_bottom.is_visited:
                    blocks_around['bottom'] = block_now_bottom
                    count += 1
            # 查看左边block
            if block_now.coordinate[0]-1 >= 0:
                block_now_left = blocks_list[block_now.coordinate[1]][block_now.coordinate[0]-1]
                if not block_now_left.is_visited:
                    blocks_around['left'] = block_now_left
                    count += 1
            # 查看右边block
            if block_now.coordinate[0]+1 < maze_size[1]:
                block_now_right = blocks_list[block_now.coordinate[1]][block_now.coordinate[0]+1]
                if not block_now_right.is_visited:
                    blocks_around['right'] = block_now_right
                    count += 1
            #上面一段把当前块的上下左右块都放入到blocks_around里了
            
            if count > 0:
                while True:
                    #随机选一个方向，把该方向上的墙打通。打通的方法就是把当前block和所选方向的下一个block的墙去掉。
                    direction = random.choice(directions)
                    if blocks_around.get(direction):
                        block_next = blocks_around.get(direction)
                        if direction == 'top':
                            #当前块的上，对应下一个block的下，注意下标
                            block_next.has_walls[1] = False
                            block_now.has_walls[0] = False
                        elif direction == 'bottom':
                            block_next.has_walls[0] = False
                            block_now.has_walls[1] = False
                        elif direction == 'left':
                            block_next.has_walls[3] = False
                            block_now.has_walls[2] = False
                        elif direction == 'right':
                            block_next.has_walls[2] = False
                            block_now.has_walls[3] = False
                        break
            #前面如果count大于0，表示上下左右至少有一个方向是没有访问过的，可以尝试打通新的方向。
            #如果count等于其初始值0，表示该节点的上下左右都访问过了，需要返回None，让尝试回退到上一步，重新选择
            return block_next

        #按照预设尺寸生成全部Block，此时的Block默认状态4面都是墙
        blocks_list = [[Block([col, row], block_size, border_size) for col in range(maze_size[1])] for row in range(maze_size[0])]
        block_now = blocks_list[0][0]
        records = []
        #在nextBlock中是随机打通墙壁的
        while True:
            if block_now:
                if not block_now.is_visited:
                    block_now.is_visited = True
                    records.append(block_now)
                    #print("forword"+str(block_now.coordinate))
                block_now = nextBlock(block_now, blocks_list)
                #屏蔽下面的if语句就可以按照完整算法生成可以到达每个格子的完美迷宫
                #如果不追求生成完美迷宫，就可以像下面这样，第一次打通了终点就退出
                #if block_now:
                #    if block_now.coordinate==[maze_size[0]-1,maze_size[0]-1]:
                #        break
            else:
                #如果上一次循环的nextBlock返回空，表示当前块四周的方向都是打通过的，要回退到上一步去。
                #如果records长度为0，表示我们已经回退到了起点，打通了到达终点的墙，迷宫生成成功。
                block_now = records.pop()
                #print("back"+str(block_now.coordinate))
                if len(records) == 0:
                    break
            #print(len(records))
        return blocks_list