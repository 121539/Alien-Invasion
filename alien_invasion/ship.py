import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其起始位置"""
        super().__init__()
        # 屏幕及其外接矩形
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load("figures/ship.bmp")
        self.rect = self.image.get_rect()
        # 每艘飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 在飞船的属性X中储存一个浮点数
        self.x = float(self.rect.x)
        # 移动标志（飞船一开始不移动）
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        # 更新飞船的属性X的值，而不是其外接矩形的属性X的值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 根据self.x更新rect对象
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)