import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    # 表示一个外星人
    
    def __init__(self, ai_setting, screen):
        # 初始化外星人，设置其原始位置
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting
        
        # 加载外星人图像并设置其rect属性
        self.image= pygame.image.load('imgs/enemy1.png')
        self.rect = self.image.get_rect()
        
        # 外星人位置初始化
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # 存储外星人当前位置
        self.x = float(self.rect.x)
    
    def blitme(self):
        # 绘制外星人
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        # 外星人位置更新
        self.x += (self.ai_setting.alien_speed_factor * self.ai_setting.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        # 检测外星人是否到达边缘
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    
    