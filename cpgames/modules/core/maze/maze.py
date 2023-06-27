'''
Function:
    走迷宫小游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import pygame
import random
from ...utils import QuitGame
from ..base import PygameBaseGame
from .modules import showText, Button, Interface, Block, RandomMaze, Hero
import copy

'''配置类'''
class Config():
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 100
    # 屏幕大小
    SCREENSIZE = (800, 625)
    # 标题
    TITLE = '走迷宫小游戏 —— Charles的皮卡丘'
    # 块大小
    BLOCKSIZE = 15
    MAZESIZE = (35, 50) # num_rows * num_cols
    #MAZESIZE = (10, 10) # num_rows * num_cols
    BORDERSIZE = (25, 50) # 25 * 2 + 50 * 15 = 800, 50 * 2 + 35 * 15 = 625
    # 背景音乐路径
    BGM_PATH = os.path.join(rootdir, 'resources/audios/bgm.mp3')
    # 游戏图片路径
    IMAGE_PATHS_DICT = {
        'hero': os.path.join(rootdir, 'resources/images/hero.png'),
    }

    
'''走迷宫小游戏'''
class MazeGame(PygameBaseGame):
    game_type = 'maze'
    def __init__(self, **kwargs):
        self.cfg = Config
        super(MazeGame, self).__init__(config=self.cfg, **kwargs)
    '''运行游戏'''
    def run(self):
        # 初始化
        screen, resource_loader, cfg = self.screen, self.resource_loader, self.cfg
        font = pygame.font.SysFont('Consolas', 15)
        # 播放背景音乐
        #resource_loader.playbgm()
        # 开始界面
        #Interface(screen, cfg, 'game_start')
        # 记录关卡数
        num_levels = 0
        # 记录每一局的步数，用于计算通关平均值
        win_step_records = []
        # 记录最少用了多少步通关
        best_scores = 'None'
        # 记录平均通关步数，用它来衡量自动算法的效果
        avg_scores = 'None'
        # 关卡循环切换
        while True:
            num_levels += 1
            clock = pygame.time.Clock()
            screen = pygame.display.set_mode(cfg.SCREENSIZE)
            # --随机生成关卡地图
            maze_now = RandomMaze(cfg.MAZESIZE, cfg.BLOCKSIZE, cfg.BORDERSIZE,screen)
            #is_visited这个标识在创建完迷宫后对迷宫就没用了，正好用在后来找出路上。
            for blockline in maze_now.blocks_list:
                for block in blockline:
                    block.is_visited = False
            # --生成hero
            hero_now = Hero(resource_loader.images['hero'], [0, 0], cfg.BLOCKSIZE, cfg.BORDERSIZE)
            # --统计步数
            num_steps = 0
            # --关卡内主循环
            path = []
            records = []
            direction_array = []
            start_point = hero_now.rect.center
            block_now = maze_now.blocks_list[0][0]
            block_now.is_visited = True
            records.append(block_now)
            path.append(hero_now.rect.center)
            '''我希望设计出自动探索迷宫，并记录下所走路径，并能把它用红色线条描绘出来的功能'''
            RED = (255,0,0)
            BG_COLOR = (199, 237, 204)

            # 选择一种自动探索算法
            method_choose = 1

            while True:
                dt = clock.tick(cfg.FPS)
                
                is_move = False
                # ----↑↓←→控制hero，只是保留原来手动玩游戏的代码，在自动模式下没用。
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        QuitGame()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            is_move = hero_now.move('up', maze_now)
                        elif event.key == pygame.K_DOWN:
                            is_move = hero_now.move('down', maze_now)
                        elif event.key == pygame.K_LEFT:
                            is_move = hero_now.move('left', maze_now)
                        elif event.key == pygame.K_RIGHT:
                            is_move = hero_now.move('right', maze_now)

                screen.fill(BG_COLOR)
                blocks_list = maze_now.blocks_list
                directions = ['up', 'down', 'left', 'right']
                blocks_around = dict(zip(directions, [None]*4))
                count = 0
                # 查看上边block，条件是判断不是最顶上的block
                if not block_now.has_walls[0]:
                    block_now_top = blocks_list[block_now.coordinate[1]-1][block_now.coordinate[0]]
                    if block_now_top.is_visited == False:
                        blocks_around['up'] = block_now_top
                        count += 1
                # 查看下边block
                if not block_now.has_walls[1]:
                    block_now_bottom = blocks_list[block_now.coordinate[1]+1][block_now.coordinate[0]]
                    if block_now_bottom.is_visited == False:
                        blocks_around['down'] = block_now_bottom
                        count += 1
                # 查看左边block
                if not block_now.has_walls[2]:
                    block_now_left = blocks_list[block_now.coordinate[1]][block_now.coordinate[0]-1]
                    if block_now_left.is_visited == False:
                        blocks_around['left'] = block_now_left
                        count += 1
                # 查看右边block
                if not block_now.has_walls[3]:
                    block_now_right = blocks_list[block_now.coordinate[1]][block_now.coordinate[0]+1]
                    if block_now_right.is_visited == False:
                        blocks_around['right'] = block_now_right
                        count += 1
                #上面一段把当前块的上下左右块都放入到blocks_around里了
                            
                if count > 0:
                    while True:
                        #怎样取得更好成绩？这里是随机选择一个方向，如果有更好的策略也许可以有更好的成绩。
                        # 方式一：随机选择一个方向
                        if method_choose==1:
                            direction = random.choice(directions)
                            if blocks_around[direction] == None:
                                continue
                                    
                        #把移动方向和当前block压栈是为了走入死胡同后可以退回来
                        direction_array.append(direction)
                        records.append(block_now)
                        block_now = blocks_around.get(direction)
                        block_now.is_visited = True
                        is_move = hero_now.move(direction, maze_now)
                        path.append(hero_now.rect.center)
                        break
                else:
                    #如果走入死胡同，从移动方向栈中弹出上一步的移动方向，反向移动回到上一步
                    pre_direction = direction_array.pop()
                    if pre_direction=='up':
                        hero_now.move('down', maze_now)
                    elif pre_direction=='down':
                        hero_now.move('up', maze_now)
                    elif pre_direction=='left':
                        hero_now.move('right', maze_now)
                    elif pre_direction=='right':
                        hero_now.move('left', maze_now)
                                
                    block_now = records.pop()
                    path.pop()                
                p1 = start_point
                for point in path:
                    pygame.draw.line( screen,RED,p1, point,2)
                    p1 = point
                
                #随机移动的代码
                '''
                while not is_move:
                    directions = ['up', 'down', 'left', 'right']
                    direction = random.choice(directions)
                    is_move = hero_now.move(direction, maze_now)

                    if is_move:
                        path.append(hero_now.rect.center)
                    
                p1 = start_point
                for point in path:
                    pygame.draw.line( screen,RED,p1, point,2)
                    p1 = point
                '''


                num_steps += int(is_move)
                hero_now.draw(screen)
                maze_now.draw(screen)
                # ----显示一些信息
                showText(screen, font, 'LEVELDONE: %d' % num_levels, (255, 0, 0), (10, 10))
                showText(screen, font, 'BESTSCORE: %s' % best_scores, (255, 0, 0), (210, 10))
                showText(screen, font, 'AVG—SCORE: %s' % avg_scores, (255, 0, 0), (410, 10))
                showText(screen, font, 'USEDSTEPS: %s' % num_steps, (255, 0, 0), (610, 10))
                showText(screen, font, 'S: your starting point    D: your destination', (255, 0, 0), (10, 600))
                # ----判断游戏是否胜利
                if (hero_now.coordinate[0] == cfg.MAZESIZE[1] - 1) and (hero_now.coordinate[1] == cfg.MAZESIZE[0] - 1):
                    break
                pygame.display.update()
            
            # 将当前局的步数记录下来，并计算平均步数
            win_step_records.append(num_steps)
            avg_scores = int(sum(win_step_records)/len(win_step_records))

            # --更新最优成绩
            if best_scores == 'None':
                best_scores = num_steps
            else:
                if best_scores > num_steps:
                    best_scores = num_steps
            # --关卡切换
            #Interface(screen, cfg, mode='game_switch')