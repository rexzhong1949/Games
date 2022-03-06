'''
Function:
    坦克类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import pygame
import random
from .foods import Foods
from .bullet import Bullet


'''智能玩家坦克类'''
class SmartPlayerTank(pygame.sprite.Sprite):
    def __init__(self, name, player_tank_images, position, border_len, screensize, direction='up', bullet_images=None, protected_mask=None, boom_image=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        # 玩家1/玩家2
        self.name = name
        # 坦克图片路径
        self.player_tank_images = player_tank_images.get(name)
        # 地图边缘宽度
        self.border_len = border_len
        # 屏幕大小
        self.screensize = screensize
        # 初始坦克方向
        self.init_direction = direction
        # 初始位置
        self.init_position = position
        # 子弹图片
        self.bullet_images = bullet_images
        # 保护罩图片路径
        self.protected_mask = protected_mask
        self.protected_mask_flash_time = 25
        self.protected_mask_flash_count = 0
        self.protected_mask_pointer = False
        # 坦克爆炸图
        self.boom_image = boom_image
        self.boom_last_time = 5
        self.booming_flag = False
        self.boom_count = 0
        # 坦克生命数量
        self.num_lifes = 3
        # 重置
        self.reset()
    '''移动'''
    def move(self, direction, scene_elems, player_tanks_group, enemy_tanks_group, home):
        # 爆炸时无法移动
        if self.booming_flag:
            return
        # 方向不一致先改变方向
        if self.direction != direction:
            self.setDirection(direction)
            self.switch_count = self.switch_time
            self.move_cache_count = self.move_cache_time
        # 移动(使用缓冲)
        self.move_cache_count += 1
        if self.move_cache_count < self.move_cache_time:
            return
        self.move_cache_count = 0
        if self.direction == 'up':
            speed = (0, -self.speed)
        elif self.direction == 'down':
            speed = (0, self.speed)
        elif self.direction == 'left':
            speed = (-self.speed, 0)
        elif self.direction == 'right':
            speed = (self.speed, 0)
        rect_ori = self.rect
        self.rect = self.rect.move(speed)
        # --碰到场景元素
        for key, value in scene_elems.items():
            if key in ['brick_group', 'iron_group', 'river_group']:
                if pygame.sprite.spritecollide(self, value, False, None):
                    self.rect = rect_ori
            elif key in ['ice_group']:
                if pygame.sprite.spritecollide(self, value, False, None):
                    self.rect = self.rect.move(speed)
        # --碰到其他玩家坦克
        if pygame.sprite.spritecollide(self, player_tanks_group, False, None):
            self.rect = rect_ori
        # --碰到敌方坦克
        if pygame.sprite.spritecollide(self, enemy_tanks_group, False, None):
            self.rect = rect_ori
        # --碰到玩家大本营
        if pygame.sprite.collide_rect(self, home):
            self.rect = rect_ori
        # --碰到边界
        if self.rect.left < self.border_len:
            self.rect.left = self.border_len
        elif self.rect.right > self.screensize[0]-self.border_len:
            self.rect.right = self.screensize[0] - self.border_len
        elif self.rect.top < self.border_len:
            self.rect.top = self.border_len
        elif self.rect.bottom > self.screensize[1]-self.border_len:
            self.rect.bottom = self.screensize[1] - self.border_len
        # 为了坦克轮动特效切换图片
        self.switch_count += 1
        if self.switch_count > self.switch_time:
            self.switch_count = 0
            self.switch_pointer = not self.switch_pointer
            self.image = self.tank_direction_image.subsurface((48*int(self.switch_pointer), 0), (48, 48))
    '''更新'''
    def update(self):
        # 坦克子弹冷却更新
        if self.is_bullet_cooling:
            self.bullet_cooling_count += 1
            if self.bullet_cooling_count >= self.bullet_cooling_time:
                self.bullet_cooling_count = 0
                self.is_bullet_cooling = False
        # 无敌状态更新
        if self.is_protected:
            self.protected_count += 1
            if self.protected_count > self.protected_time:
                self.is_protected = False
                self.protected_count = 0
        # 爆炸状态更新
        if self.booming_flag:
            self.image = self.boom_image
            self.boom_count += 1
            if self.boom_count > self.boom_last_time:
                self.boom_count = 0
                self.booming_flag = False
                self.reset()
    '''设置坦克方向'''
    def setDirection(self, direction):
        self.direction = direction
        if self.direction == 'up':
            self.tank_direction_image = self.tank_image.subsurface((0, 0), (96, 48))
        elif self.direction == 'down':
            self.tank_direction_image = self.tank_image.subsurface((0, 48), (96, 48))
        elif self.direction == 'left':
            self.tank_direction_image = self.tank_image.subsurface((0, 96), (96, 48))
        elif self.direction == 'right':
            self.tank_direction_image = self.tank_image.subsurface((0, 144), (96, 48))
    '''射击'''
    def shoot(self):
        # 爆炸时无法射击
        if self.booming_flag:
            return False
        # 子弹不在冷却状态时
        if not self.is_bullet_cooling:
            self.is_bullet_cooling = True
            if self.tanklevel == 0:
                is_stronger = False
                speed = 8
            elif self.tanklevel == 1:
                is_stronger = False
                speed = 10
            elif self.tanklevel >= 2:
                is_stronger = True
                speed = 10
            if self.direction == 'up':
                position = (self.rect.centerx, self.rect.top-1)
            elif self.direction == 'down':
                position = (self.rect.centerx, self.rect.bottom+1)
            elif self.direction == 'left':
                position = (self.rect.left-1, self.rect.centery)
            elif self.direction == 'right':
                position = (self.rect.right+1, self.rect.centery)
            return Bullet(bullet_images=self.bullet_images, screensize=self.screensize, direction=self.direction, position=position, border_len=self.border_len, is_stronger=is_stronger, speed=speed)
        return False
    '''提高坦克等级'''
    def improveTankLevel(self):
        if self.booming_flag:
            return False
        self.tanklevel = min(self.tanklevel+1, len(self.player_tank_images)-1)
        self.tank_image = self.player_tank_images[self.tanklevel].convert_alpha()
        self.setDirection(self.direction)
        self.image = self.tank_direction_image.subsurface((48*int(self.switch_pointer), 0), (48, 48))
        return True
    '''降低坦克等级'''
    def decreaseTankLevel(self):
        if self.booming_flag:
            return False
        self.tanklevel -= 1
        if self.tanklevel < 0:
            self.num_lifes -= 1
            self.booming_flag = True
        else:
            self.tank_image = self.player_tank_images[self.tanklevel].convert_alpha()
            self.setDirection(self.direction)
            self.image = self.tank_direction_image.subsurface((48*int(self.switch_pointer), 0), (48, 48))
        return True if self.tanklevel < 0 else False
    '''增加生命值'''
    def addLife(self):
        self.num_lifes += 1
    '''设置为无敌状态'''
    def setProtected(self):
        self.is_protected = True
    '''画我方坦克'''
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.is_protected:
            self.protected_mask_flash_count += 1
            if self.protected_mask_flash_count > self.protected_mask_flash_time:
                self.protected_mask_pointer = not self.protected_mask_pointer
                self.protected_mask_flash_count = 0
            screen.blit(self.protected_mask.subsurface((48*self.protected_mask_pointer, 0), (48, 48)), self.rect)
    '''重置坦克, 重生的时候用'''
    def reset(self):
        # 坦克方向
        self.direction = self.init_direction
        # 移动缓冲, 用于避免坦克连续运行不方便调整位置
        self.move_cache_time = 4
        self.move_cache_count = 0
        # 是否无敌状态
        self.is_protected = False
        self.protected_time = 1500
        self.protected_count = 0
        # 坦克移动速度
        self.speed = 8
        # 子弹冷却时间
        self.bullet_cooling_time = 30
        self.bullet_cooling_count = 0
        self.is_bullet_cooling = False
        # 坦克等级
        self.tanklevel = 0
        # 坦克轮子转动效果
        self.switch_count = 0
        self.switch_time = 1
        self.switch_pointer = False
        # 坦克图片
        self.tank_image = self.player_tank_images[self.tanklevel].convert_alpha()
        self.setDirection(self.direction)
        self.image = self.tank_direction_image.subsurface((48*int(self.switch_pointer), 0), (48, 48))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.init_position


