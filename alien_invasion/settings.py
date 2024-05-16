class Settings:
    """储存游戏中所有的设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船的设置
        self.ship_limit = 2
        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        # 子弹数量限制
        self.bullet_allowed = 15
        # 外星人设置
        # 到达屏幕边缘，外星人向下移动的速度
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移动，为-1表示向左2移动
        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        # 外星人分数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的量"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        # fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1
        # 计分设置
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置的值和外星人的分数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)



