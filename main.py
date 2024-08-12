import pygame
from setting import Setting
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    pygame.init()
    ai_setting = Setting()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("Invasion")
    # 创建play按钮
    play_button = Button(ai_setting,screen,"Play")
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_setting)
    # 创建一个记分牌
    sb = Scoreboard(ai_setting,screen,stats)
    # 创建一个飞船
    ship = Ship(ai_setting,screen)
    bullets = Group()
    # 创建一个外星人
    aliens = Group()
    gf.create_fleet(ai_setting, screen,ship, aliens)
    while True:
        gf.check_events(ai_setting, screen,stats,sb,play_button, ship,aliens,bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_setting, screen,stats,sb, ship, aliens, bullets)
            gf.update_aliens(ai_setting,stats,sb,screen,ship,aliens,bullets)
        
        gf.update_screen(ai_setting, screen,stats,sb, ship, aliens, bullets,play_button)
    
run_game()          