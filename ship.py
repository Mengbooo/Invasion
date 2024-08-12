import pygame
from pygame.sprite import Sprite
 
class Ship(Sprite):
    def __init__(self, ai_setting ,screen):
        super(Ship,self).__init__()
        # 初始化飞船并设置其初始位置
        self.screen = screen
        self.ai_setting = ai_setting
        self.image = pygame.image.load("imgs/life.png")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
         
        # 飞船位置初始化
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
         
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False  
        self.moving_down = False  
       
         
         
    def update(self):
        # 根据移动标志调整飞船的位置
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_setting.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_setting.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.rect.top -= self.ai_setting.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.bottom += self.ai_setting.ship_speed_factor
        # 根据self.center更新rect.centerx
        self.rect.centerx = self.center
         
    def blitme(self):
        # 在指定位置绘制飞船图片
        self.screen.blit(self.image,self.rect)
        
    def center_ship(self):
    # 让飞船在屏幕底部居中
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    