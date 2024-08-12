import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def fire_bullets(ai_setting, screen, ship, bullets):
    if len(bullets) < ai_setting.bullets_allowed:
            new_bullet = Bullet(ai_setting, screen, ship)
            bullets.add(new_bullet)

def update_bullets(ai_setting,screen,stats,sb,ship,aliens, bullets):
    # 更新子弹位置
    bullets.update()
   
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting, screen,stats,sb, ship, aliens, bullets)
    
def check_bullet_alien_collisions(ai_setting, screen,stats,sb, ship, aliens, bullets):
    # 检测子弹和外星人碰撞
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    
    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_setting, screen, ship, aliens)
        
def check_keydown_events(event, ai_setting, screen, ship, bullets):
    # 响应按键事件
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_setting, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
       
              
def check_keyup_events(event,ship):
    # 响应松开事件
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
        
    
def check_events(ai_setting, screen,stats,sb,play_button, ship,aliens, bullets):
    # 相应鼠标和键盘事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_setting, screen, ship, bullets)
          
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting,screen,stats,sb,play_button,ship,aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_setting,screen,stats,sb,play_button,ship,aliens, bullets, mouse_x, mouse_y):
    button_clicked  = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 响应play按钮点击事件
    if button_clicked and not stats.game_active:
        ai_setting.initialize_dynamic_setting()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        
        aliens.empty()
        bullets.empty()
        create_fleet(ai_setting,screen,ship,aliens)
        ship.center_ship()
               
def update_screen(ai_setting, screen,stats,sb, ship,aliens, bullets, play_button):
    # 刷新屏幕
    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()
    
def create_fleet(ai_setting, screen, ship, aliens):
    # 创建外星人群
    alien = Alien(ai_setting , screen)
    number_aliens_x = get_number_aliens_x(ai_setting,alien.rect.width)
    number_rows = get_number_rows(ai_setting,ship.rect.height,alien.rect.height)
    for alien_number in range(number_aliens_x):
        for row_number in range(number_rows):
            create_alien(ai_setting,screen,aliens,alien_number,row_number)
        
def get_number_aliens_x(ai_setting,lien_width):
    # 计算屏幕可容纳多少个外星人
    available_space_x = ai_setting.screen_width - (2 * lien_width)
    number_aliens_x = int(available_space_x / (2 * lien_width))
    return number_aliens_x

def get_number_rows(ai_setting,ship_height,alien_height):
    # 计算屏幕可容纳多少行外星人
    available_space_y = (ai_setting.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_setting,screen,aliens,alien_number,row_number):
    # 创建单个外星人
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def update_aliens(ai_setting,stats,sb,screen,ship,aliens,bullets):
    check_fleet_edges(ai_setting, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting,stats, screen, ship, aliens, bullets)
        
    check_aliens_bottom(ai_setting,stats,sb, screen, ship, aliens, bullets)
    
def check_fleet_edges(ai_setting, aliens):
    # 边缘检测
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break
        
def change_fleet_direction(ai_setting, aliens):
    # 改变外星人群方向
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1

def ship_hit(ai_setting,stats,sb, screen, ship, aliens, bullets):
    # 处理被外星人撞到的飞船
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        sleep(0.5)
        aliens.empty()
        bullets.empty()
        create_fleet(ai_setting, screen, ship, aliens)
        ship.center_ship()
    elif stats.ships_left == 0:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        

    
def check_aliens_bottom(ai_setting,stats,sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 处理被外星人撞到的飞船
            ship_hit(ai_setting,stats, screen,sb, ship, aliens, bullets)
            break

def check_high_score(stats,sb) :
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()