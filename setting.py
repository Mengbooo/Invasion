class Setting:
    
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 900
        self.bg_color = (230 ,230 ,230)
        # 飞船设置
        self.ship_limit = 3
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0 ,0 ,0)
        self.bullets_allowed = 3
        # 外星人设置
        self.fleet_drop_speed = 5
        self.speedup_scale = 1.2
        self.score_scale = 1.5
        self.initialize_dynamic_setting()
        
    def initialize_dynamic_setting(self):
        self.ship_speed_factor = 0.6
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 0.2
        
        self.alien_points = 50
        self.fleet_direction = 1
        
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)