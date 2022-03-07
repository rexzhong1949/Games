'''
Function:
    用于运行某一游戏关卡
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
from pickle import TRUE
from tkinter import CENTER
from typing import Dict
import pygame
import random
from .sprites import *
from ....utils import QuitGame


'''用于运行某一游戏关卡'''
class GameLevel():
    def __init__(self, gamelevel, levelfilepath, is_dual_mode, cfg, resource_loader, **kwargs):
        self.cfg = cfg
        # 关卡地图路径
        self.gamelevel = gamelevel
        self.levelfilepath = levelfilepath
        # 资源加载器
        self.resource_loader = resource_loader
        self.sounds = self.resource_loader.sounds
        # 是否为双人模式
        self.is_dual_mode = is_dual_mode
        # 地图规模参数
        self.border_len = cfg.BORDER_LEN
        self.grid_size = cfg.GRID_SIZE
        self.width, self.height = cfg.SCREENSIZE
        self.panel_width = cfg.PANEL_WIDTH
        # 字体
        self.font = resource_loader.fonts['gaming']
        # 关卡场景元素
        self.scene_elems = {
            'brick_group': pygame.sprite.Group(), 
            'iron_group': pygame.sprite.Group(),
            'ice_group': pygame.sprite.Group(), 
            'river_group': pygame.sprite.Group(),
            'tree_group': pygame.sprite.Group()
        }

        self.speed = 8
        # 解析关卡文件
        self.__parseLevelFile()
    '''
    #最简单的策略，追着第一个敌方坦克，先到同样高度，再追着打
    def smarttank_move(self, scene_elems:Dict, player_tanks_group:pygame.sprite.Group, enemy_tanks_group:pygame.sprite.Group, home:Home ):
        smarttank_dir = "STOP"
        smarttank = player_tanks_group.sprites()[1]
        if len(enemy_tanks_group)>0:
            enemytank = enemy_tanks_group.sprites()[0]
            if enemytank.rect.top < smarttank.rect.top:
                smarttank_dir = "UP"
            elif enemytank.rect.top > smarttank.rect.top:
                smarttank_dir = "DOWN"
            elif enemytank.rect.left < smarttank.rect.left:
                smarttank_dir = "LEFT"
            elif enemytank.rect.left > smarttank.rect.left:
                smarttank_dir = "RIGHT"
                
        smarttank_shoot = True
        return smarttank_dir,smarttank_shoot
    '''
    
    '''
    #第二种策略，追着打第一个敌方坦克，缩小水平和垂直距离
    def smarttank_move(self, scene_elems:Dict, player_tanks_group:pygame.sprite.Group, enemy_tanks_group:pygame.sprite.Group, home:Home ):
        smarttank_dir = "STOP"
        smarttank = player_tanks_group.sprites()[1]
        if len(enemy_tanks_group)>0:
            enemytank = enemy_tanks_group.sprites()[0]
            x_distans = (enemytank.rect.left-smarttank.rect.left)**2
            y_distans = (enemytank.rect.top-smarttank.rect.top)**2
            if ( x_distans>y_distans):
                if enemytank.rect.left < smarttank.rect.left:
                    smarttank_dir = "LEFT"
                elif enemytank.rect.left > smarttank.rect.left:
                    smarttank_dir = "RIGHT"
            else:
                if enemytank.rect.top < smarttank.rect.top:
                    smarttank_dir = "UP"
                elif enemytank.rect.top > smarttank.rect.top:
                    smarttank_dir = "DOWN"
                
        smarttank_shoot = True
        return smarttank_dir,smarttank_shoot
    '''
    
    '''
    #第三个策略，追着离家最近的坦克打，效果比前两个好
    def smarttank_move(self, scene_elems:Dict, player_tanks_group:pygame.sprite.Group, enemy_tanks_group:pygame.sprite.Group, home:Home ):
        smarttank_dir = "STOP"
        smarttank = player_tanks_group.sprites()[1]

        if len(enemy_tanks_group)>0:
            most_threaten = enemy_tanks_group.sprites()[0]
            most_near_distance = 1000000000000
            for enemytank in enemy_tanks_group.sprites():
                distance_to_home = (enemytank.rect.centerx-home.rect.centerx)**2 + (enemytank.rect.centery-home.rect.centery)**2
                if distance_to_home<most_near_distance:
                    most_threaten = enemytank

            x_distans = (most_threaten.rect.left-smarttank.rect.left)**2
            y_distans = (most_threaten.rect.top-smarttank.rect.top)**2
            if ( x_distans>y_distans):
                if most_threaten.rect.left < smarttank.rect.left:
                    smarttank_dir = "LEFT"
                elif most_threaten.rect.left > smarttank.rect.left:
                    smarttank_dir = "RIGHT"
            else:
                if most_threaten.rect.top < smarttank.rect.top:
                    smarttank_dir = "UP"
                elif most_threaten.rect.top > smarttank.rect.top:
                    smarttank_dir = "DOWN"
                
        smarttank_shoot = True
        return smarttank_dir,smarttank_shoot
    '''

    #第四个策略，还是追着离家最近的坦克打，希望解决被障碍卡住的问题
    def smarttank_move(self, player, screen,scene_elems:Dict, player_tanks_group:pygame.sprite.Group, enemy_tanks_group:pygame.sprite.Group, home:Home ):
        smarttank_dir = "STOP"

        #这里比较郁闷，在外部有对player_tanks_group的add和remove，每次进来这里调用
        #两个坦克的顺序都交换过，看了好久打印才发现
        smarttank = player_tanks_group.sprites()[0]
        #print(smarttank.rect)

        if len(enemy_tanks_group)>0:
            most_threaten = enemy_tanks_group.sprites()[0]
            most_near_distance = 1000000000000
            for enemytank in enemy_tanks_group.spritedict:
                distance_to_home = (enemytank.rect.centerx-home.rect.centerx)**2 + (enemytank.rect.centery-home.rect.centery)**2
                if distance_to_home<most_near_distance:
                    most_threaten = enemytank
                    most_near_distance = distance_to_home
            speed = (0,0)
            x_distans = (most_threaten.rect.left-smarttank.rect.left)**2
            y_distans = (most_threaten.rect.top-smarttank.rect.top)**2
            if ( x_distans>y_distans):
                if most_threaten.rect.left < smarttank.rect.left:
                    smarttank_dir = "LEFT"
                    speed = (-self.speed, 0)
                elif most_threaten.rect.left > smarttank.rect.left:
                    smarttank_dir = "RIGHT"
                    speed = (self.speed, 0)
            else:
                if most_threaten.rect.top < smarttank.rect.top:
                    smarttank_dir = "UP"
                    speed = (0, -self.speed)
                elif most_threaten.rect.top > smarttank.rect.top:
                    smarttank_dir = "DOWN"
                    speed = (0, self.speed)

            pygame.draw.rect( screen, (255,0,0),most_threaten.rect,5)
            pygame.draw.line( screen,(255,0,0),home.rect.center,most_threaten.rect.center,5)

            rect_ori = smarttank.rect
            smarttank.rect = smarttank.rect.move(speed)
            # 如果碰到场景元素卡住，跟踪目标方向进行摆脱。
            for key, value in scene_elems.items():
                if key in ['brick_group', 'iron_group', 'river_group']:
                    if pygame.sprite.spritecollide(smarttank, value, False, None):
                        #如果想左右移动被卡住，则需要上下移动，跟着目标的方向
                        if smarttank_dir == "LEFT" or smarttank_dir == "RIGHT":
                            if smarttank.rect.top > most_threaten.rect.top:
                                smarttank_dir = "UP"
                            else:
                                smarttank_dir = "DOWN"    
                        #如果想上下移动被卡住，则需要左右移动，跟着目标的方向
                        elif smarttank_dir == "UP" or smarttank_dir == "DOWN":
                            if smarttank.rect.left > most_threaten.rect.left:
                                smarttank_dir = "LEFT"
                            else:
                                smarttank_dir = "RIGHT"    
            #以上只能判断，不能真的移动smarttank，所以要恢复其位置，先前暂存在rect_ori里的
            smarttank.rect = rect_ori
        #为避免自己打基地，简单的不能瞄准home开枪
        if (smarttank.rect.centery < home.rect.top) and (smarttank.rect.centerx < home.rect.left or smarttank.rect.centerx > home.rect.right):
            smarttank_shoot = True
        else:
            smarttank_shoot = False
       
        return smarttank_dir,smarttank_shoot


    '''开始游戏'''
    def start(self, screen):
        screen, resource_loader = pygame.display.set_mode((self.width+self.panel_width, self.height)), self.resource_loader
        # 背景图片
        background_img = resource_loader.images['others']['background']
        # 定义精灵组
        player_tanks_group = pygame.sprite.Group()
        enemy_tanks_group = pygame.sprite.Group()
        player_bullets_group = pygame.sprite.Group()
        enemy_bullets_group = pygame.sprite.Group()
        foods_group = pygame.sprite.Group()
        # 定义敌方坦克生成事件
        generate_enemies_event = pygame.constants.USEREVENT
        pygame.time.set_timer(generate_enemies_event, 5000)
        # 我方大本营
        home = Home(position=self.home_position, images=resource_loader.images['home'])
        # 我方坦克
        tank_player1 = SmartPlayerTank(
            name='player1', position=self.player_tank_positions[0], player_tank_images=resource_loader.images['player'], 
            border_len=self.border_len, screensize=[self.width, self.height], bullet_images=resource_loader.images['bullet'], 
            protected_mask=resource_loader.images['others']['protect'], boom_image=resource_loader.images['others']['boom_static']
        )
        player_tanks_group.add(tank_player1)
        if self.is_dual_mode:
            tank_player2 = SmartPlayerTank(
                name='player2', position=self.player_tank_positions[1], player_tank_images=resource_loader.images['player'], 
                border_len=self.border_len, screensize=[self.width, self.height], bullet_images=resource_loader.images['bullet'], 
                protected_mask=resource_loader.images['others']['protect'], boom_image=resource_loader.images['others']['boom_static']
            )
            player_tanks_group.add(tank_player2)
        # 敌方坦克
        for position in self.enemy_tank_positions:
            enemy_tanks_group.add(EnemyTank(
                enemy_tank_images=resource_loader.images['enemy'], appear_image=resource_loader.images['others']['appear'], position=position, 
                border_len=self.border_len, screensize=[self.width, self.height], bullet_images=resource_loader.images['bullet'], 
                food_images=resource_loader.images['food'], boom_image=resource_loader.images['others']['boom_static']
            ))
        # 游戏开始音乐
        #self.sounds['start'].play()
        clock = pygame.time.Clock()
        # 该关卡通过与否的flags
        is_win = False
        is_running = True
        # 游戏主循环
        while is_running:
            screen.fill((0, 0, 0))
            screen.blit(background_img, (0, 0))

            #试图放入按键事件，没有成功，直接修改key_pressed数组
            #uevent=pygame.event.Event(pygame.KEYDOWN,{"key":pygame.K_UP})
            #pygame.event.post(uevent)
            
            # 用户事件捕捉
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    QuitGame()
                # --敌方坦克生成
                elif event.type == generate_enemies_event:
                    if self.max_enemy_num > len(enemy_tanks_group):
                        for position in self.enemy_tank_positions:
                            if len(enemy_tanks_group) == self.total_enemy_num:
                                break
                            enemy_tank = EnemyTank(
                                enemy_tank_images=resource_loader.images['enemy'], appear_image=resource_loader.images['others']['appear'], position=position, 
                                border_len=self.border_len, screensize=[self.width, self.height], bullet_images=resource_loader.images['bullet'], 
                                food_images=resource_loader.images['food'], boom_image=resource_loader.images['others']['boom_static']
                            )
                            if (not pygame.sprite.spritecollide(enemy_tank, enemy_tanks_group, False, None)) and (not pygame.sprite.spritecollide(enemy_tank, player_tanks_group, False, None)):
                                enemy_tanks_group.add(enemy_tank)
            # --用户按键
            key_pressed = pygame.key.get_pressed()
            
            smarttank_dir = "STOP"
            smarttank_shoot = False
            # 玩家一, WSAD移动, 空格键射击
            smarttank_dir,smarttank_shoot = self.smarttank_move( 1,screen,self.scene_elems, player_tanks_group, enemy_tanks_group, home)
            if self.is_dual_mode and (tank_player1.num_lifes >= 0):
                #if key_pressed[pygame.K_UP]:
                if smarttank_dir == "UP":
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('up', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                #elif key_pressed[pygame.K_DOWN]:
                elif smarttank_dir == "DOWN":
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('down', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                #elif key_pressed[pygame.K_LEFT]:
                elif smarttank_dir == "LEFT":
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('left', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                #elif key_pressed[pygame.K_RIGHT]:
                elif smarttank_dir == "RIGHT":
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('right', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)

                #elif key_pressed[pygame.K_KP0]:
                if smarttank_shoot == True:
                    smarttank_shoot = False
                    bullet = tank_player1.shoot()
                    if bullet:
                        player_bullets_group.add(bullet)
                        #self.sounds['fire'].play() if tank_player1.tanklevel < 2 else self.sounds['Gunfire'].play()
            
            smarttank_dir2 = "STOP"
            smarttank_shoot2 = False
            # 玩家二, ↑↓←→移动, 小键盘0键射击
            smarttank_dir2,smarttank_shoot2 = self.smarttank_move( 2,screen,self.scene_elems, player_tanks_group, enemy_tanks_group, home)
            if self.is_dual_mode and (tank_player2.num_lifes >= 0):
                #if key_pressed[pygame.K_UP]:
                if smarttank_dir2 == "UP":
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('up', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                #elif key_pressed[pygame.K_DOWN]:
                elif smarttank_dir2 == "DOWN":
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('down', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                #elif key_pressed[pygame.K_LEFT]:
                elif smarttank_dir2 == "LEFT":
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('left', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                #elif key_pressed[pygame.K_RIGHT]:
                elif smarttank_dir2 == "RIGHT":
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('right', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)

                #elif key_pressed[pygame.K_KP0]:
                if smarttank_shoot2 == True:
                    smarttank_shoot2 = False
                    bullet = tank_player2.shoot()
                    if bullet:
                        player_bullets_group.add(bullet)
                        #self.sounds['fire'].play() if tank_player2.tanklevel < 2 else self.sounds['Gunfire'].play()
            # 碰撞检测
            # --子弹和砖墙
            pygame.sprite.groupcollide(player_bullets_group, self.scene_elems.get('brick_group'), True, True)
            pygame.sprite.groupcollide(enemy_bullets_group, self.scene_elems.get('brick_group'), True, True)
            # --子弹和铁墙
            for bullet in player_bullets_group:
                if pygame.sprite.spritecollide(bullet, self.scene_elems.get('iron_group'), bullet.is_stronger, None):
                    player_bullets_group.remove(bullet)
            pygame.sprite.groupcollide(enemy_bullets_group, self.scene_elems.get('iron_group'), True, False)
            # --子弹撞子弹
            pygame.sprite.groupcollide(player_bullets_group, enemy_bullets_group, True, True)
            # --我方子弹撞敌方坦克
            for tank in enemy_tanks_group:
                if pygame.sprite.spritecollide(tank, player_bullets_group, True, None):
                    if tank.food:
                        foods_group.add(tank.food)
                        tank.food = None
                    if tank.decreaseTankLevel():
                        self.sounds['bang'].play()
                        self.total_enemy_num -= 1
            # --敌方子弹撞我方坦克
            for tank in player_tanks_group:
                if pygame.sprite.spritecollide(tank, enemy_bullets_group, True, None):
                    if tank.is_protected:
                        self.sounds['blast'].play()
                    else:
                        if tank.decreaseTankLevel():
                            self.sounds['bang'].play()
                        if tank.num_lifes < 0:
                            player_tanks_group.remove(tank)
            # --我方子弹撞我方大本营
            if pygame.sprite.spritecollide(home, player_bullets_group, True, None):
                is_win = False
                is_running = False
                home.setDead()
            # --敌方子弹撞我方大本营
            if pygame.sprite.spritecollide(home, enemy_bullets_group, True, None):
                is_win = False
                is_running = False
                home.setDead()
            # --我方坦克在植物里
            if pygame.sprite.groupcollide(player_tanks_group, self.scene_elems.get('tree_group'), False, False):
                self.sounds['hit'].play()
            # --我方坦克吃到食物
            for player_tank in player_tanks_group:
                for food in foods_group:
                    if pygame.sprite.collide_rect(player_tank, food):
                        if food.name == 'boom':
                            self.sounds['add'].play()
                            for _ in enemy_tanks_group:
                                self.sounds['bang'].play()
                            self.total_enemy_num -= len(enemy_tanks_group)
                            enemy_tanks_group = pygame.sprite.Group()
                        elif food.name == 'clock':
                            self.sounds['add'].play()
                            for enemy_tank in enemy_tanks_group:
                                enemy_tank.setStill()
                        elif food.name == 'gun':
                            self.sounds['add'].play()
                            player_tank.improveTankLevel()
                        elif food.name == 'iron':
                            self.sounds['add'].play()
                            self.__pretectHome()
                        elif food.name == 'protect':
                            self.sounds['add'].play()
                            player_tank.setProtected()
                        elif food.name == 'star':
                            self.sounds['add'].play()
                            player_tank.improveTankLevel()
                            player_tank.improveTankLevel()
                        elif food.name == 'tank':
                            self.sounds['add'].play()
                            player_tank.addLife()
                        foods_group.remove(food)
            # 画场景地图
            for key, value in self.scene_elems.items():
                if key in ['ice_group', 'river_group']:
                    value.draw(screen)
            # 更新并画我方子弹
            for bullet in player_bullets_group:
                if bullet.move():
                    player_bullets_group.remove(bullet)
            player_bullets_group.draw(screen)
            # 更新并画敌方子弹
            for bullet in enemy_bullets_group:
                if bullet.move():
                    enemy_bullets_group.remove(bullet)
            enemy_bullets_group.draw(screen)
            # 更新并画我方坦克
            for tank in player_tanks_group:
                tank.update()
                tank.draw(screen)
            # 更新并画敌方坦克
            for tank in enemy_tanks_group:
                enemy_tanks_group.remove(tank)
                data_return = tank.update(self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                enemy_tanks_group.add(tank)
                if data_return.get('bullet'):
                    enemy_bullets_group.add(data_return.get('bullet'))
                if data_return.get('boomed'):
                    enemy_tanks_group.remove(tank)
            enemy_tanks_group.draw(screen)
            # 画场景地图
            for key, value in self.scene_elems.items():
                if key not in ['ice_group', 'river_group']:
                    value.draw(screen)
            # 画大本营
            home.draw(screen)
            # 更新并显示食物
            for food in foods_group:
                if food.update():
                    foods_group.remove(food)
            foods_group.draw(screen)
            self.__showGamePanel(screen, tank_player1, tank_player2) if self.is_dual_mode else self.__showGamePanel(screen, tank_player1)
            # 我方坦克都挂了
            if len(player_tanks_group) == 0:
                is_win = False
                is_running = False
            # 敌方坦克都挂了
            if self.total_enemy_num <= 0:
                is_win = True
                is_running = False
            pygame.display.flip()
            clock.tick(self.cfg.FPS)
        screen = pygame.display.set_mode((self.width, self.height))
        return is_win
    '''显示游戏面板'''
    def __showGamePanel(self, screen, tank_player1, tank_player2=None):
        color_white = (255, 255, 255)
        # 玩家一操作提示
        player1_operate_tip = self.font.render('Operate-P1:', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_w: Up', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*2/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_s: Down', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*3/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_a: Left', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*4/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_d: Right', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*5/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_SPACE: Shoot', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*6/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        # 玩家二操作提示
        player2_operate_tip = self.font.render('Operate-P2:', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*8/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_UP: Up', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*9/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_DOWN: Down', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*10/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_LEFT: Left', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*11/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_RIGHT: Right', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*12/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_KP0: Shoot', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*13/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        # 玩家一状态提示
        player1_state_tip = self.font.render('State-P1:', True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*15/30
        screen.blit(player1_state_tip, player1_state_tip_rect)
        player1_state_tip = self.font.render('Life: %s' % tank_player1.num_lifes, True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*16/30
        screen.blit(player1_state_tip, player1_state_tip_rect)
        player1_state_tip = self.font.render('TLevel: %s' % tank_player1.tanklevel, True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*17/30
        screen.blit(player1_state_tip, player1_state_tip_rect)
        # 玩家二状态提示
        player2_state_tip = self.font.render('State-P2:', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*19/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        player2_state_tip = self.font.render('Life: %s' % tank_player2.num_lifes, True, color_white) if tank_player2 else self.font.render('Life: None', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*20/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        player2_state_tip = self.font.render('TLevel: %s' % tank_player2.tanklevel, True, color_white) if tank_player2 else self.font.render('TLevel: None', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*21/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        # 当前关卡
        game_level_tip = self.font.render('Game Level: %s' % self.gamelevel, True, color_white)
        game_level_tip_rect = game_level_tip.get_rect()
        game_level_tip_rect.left, game_level_tip_rect.top = self.width+5, self.height*23/30
        screen.blit(game_level_tip, game_level_tip_rect)
        # 剩余敌人数量
        remaining_enemy_tip = self.font.render('Remain Enemy: %s' % self.total_enemy_num, True, color_white)
        remaining_enemy_tip_rect = remaining_enemy_tip.get_rect()
        remaining_enemy_tip_rect.left, remaining_enemy_tip_rect.top = self.width+5, self.height*24/30
        screen.blit(remaining_enemy_tip, remaining_enemy_tip_rect)
    '''保护大本营'''
    def __pretectHome(self):
        for x, y in self.home_around_positions:
            self.scene_elems['iron_group'].add(Iron((x, y), self.resource_loader.images['scene']['iron']))
    '''解析关卡文件'''
    def __parseLevelFile(self):
        f = open(self.levelfilepath, errors='ignore')
        num_row = -1
        for line in f.readlines():
            line = line.strip('\n')
            # 注释
            if line.startswith('#') or (not line):
                continue
            # 敌方坦克总数量
            elif line.startswith('%TOTALENEMYNUM'):
                self.total_enemy_num = int(line.split(':')[-1])
            # 场上敌方坦克最大数量
            elif line.startswith('%MAXENEMYNUM'):
                self.max_enemy_num = int(line.split(':')[-1])
                print( "max enemy:"+str(self.max_enemy_num))
            # 大本营位置
            elif line.startswith('%HOMEPOS'):
                self.home_position = line.split(':')[-1]
                self.home_position = [int(self.home_position.split(',')[0]), int(self.home_position.split(',')[1])]
                self.home_position = (self.border_len+self.home_position[0]*self.grid_size, self.border_len+self.home_position[1]*self.grid_size)
            # 大本营周围位置
            elif line.startswith('%HOMEAROUNDPOS'):
                self.home_around_positions = line.split(':')[-1]
                self.home_around_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.home_around_positions.split(' ')]
                self.home_around_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.home_around_positions]
            # 我方坦克初始位置
            elif line.startswith('%PLAYERTANKPOS'):
                self.player_tank_positions = line.split(':')[-1]
                self.player_tank_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.player_tank_positions.split(' ')]
                self.player_tank_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.player_tank_positions]
            # 敌方坦克初始位置
            elif line.startswith('%ENEMYTANKPOS'):
                self.enemy_tank_positions = line.split(':')[-1]
                self.enemy_tank_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.enemy_tank_positions.split(' ')]
                self.enemy_tank_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.enemy_tank_positions]
            # 地图元素
            else:
                num_row += 1
                for num_col, elem in enumerate(line.split(' ')):
                    position = self.border_len+num_col*self.grid_size, self.border_len+num_row*self.grid_size
                    if elem == 'B':
                        self.scene_elems['brick_group'].add(Brick(position, self.resource_loader.images['scene']['brick']))
                    elif elem == 'I':
                        self.scene_elems['iron_group'].add(Iron(position, self.resource_loader.images['scene']['iron']))
                    elif elem == 'R':
                        self.scene_elems['river_group'].add(River(position, random.choice([self.resource_loader.images['scene']['river1'], self.resource_loader.images['scene']['river2']])))
                    elif elem == 'C':
                        self.scene_elems['ice_group'].add(Ice(position, self.resource_loader.images['scene']['ice']))
                    elif elem == 'T':
                        self.scene_elems['tree_group'].add(Tree(position, self.resource_loader.images['scene']['tree']))