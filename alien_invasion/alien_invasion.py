import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import Gamestats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 初始化pygame
        pygame.init()
        # 控制帧率
        self.clock = pygame.time.Clock()
        # 创建setting实例（将实例用作属性）
        self.settings = Settings()
        # 绘制整个游戏窗口(用户定义窗口大小)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 全屏
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.sereen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # 创建飞船（实例做属性）
        self.ship = Ship(self)
        # 储存子弹的编组
        self.bullets = pygame.sprite.Group()
        # 创建外星人编组
        self.aliens = pygame.sprite.Group()
        # 创建外星舰队(辅助函数)
        self._create_fleet()
        # 创建一个用于统计储存游戏统计信息的实例
        self.stats = Gamestats(self)
        # 标志位，游戏启动时为True(游戏开始时为False)
        self.game_active = False
        # 创建Play按钮
        self.play_button = Button(self, "play")
        # 创建储存游戏统计信息的实例，并创建记分牌
        self.sb = Scoreboard(self)

    def run_game(self):
        """开始游戏主循环"""
        while True:
            # 侦听键盘和鼠标
            self._check_events()
            if self.game_active:
                # 更新飞船位置
                self.ship.update()
                # 更新子弹位置 # 删除已消失的子弹
                self.update_bullets()
                # 更新子弹后，更新外星人的位置
                self._update_aliens()
            # 让最近绘制的屏幕可见，更新屏幕  # 每次循环时都重绘屏幕
            self._update_screen()
            # 帧数为60帧
            self.clock.tick(60)

    def _check_events(self):
        """响应按键和鼠标事件（辅助方法）"""
        for event in pygame.event.get():
            # 检测窗口关闭按钮
            if event.type == pygame.QUIT:
                sys.exit()
            # 按下方向键，移动
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # 松开方向键，停止
            elif event.type == pygame.KEYUP:
                self.__check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按下(辅助方法)"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def __check_keyup_events(self, event):
        """响应释放（辅助方法）"""
        # 右方向键
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        # 左方向键
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # 还原游戏的值
            self.settings.initialize_dynamic_settings()
            # 重置游戏的统计信息
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏光标
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        # 检查子弹数量是否已经超过了允许值
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullets(self):
        """更新子弹的位置并删除已经消失的子弹"""
        # 更新子弹位置
        self.bullets.update()
        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _create_fleet(self):
        """创建一个外星人舰队"""
        # 创建一个外星人,并不断添加，直到没有空间添加外星人为止
        # 外星人的间距为外星人的宽度和高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        # 嵌套循环，在屏幕宽度和高度方向上铺满外星人
        while current_y < (self.settings.screen_height - 3*alien_height):
            while current_x < (self.settings.screen_width - 2*alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width
            # 添加一行后，重置x值并递增y值
            current_x = alien_width
            current_y += 3*alien_height

    def _create_alien(self, x_position,y_position):
        """创建一个外星人并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        # 加入编组
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """在外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            # 如果到达屏幕边缘，返回True
            if alien.check_edges():
                # 到达边缘退出循环，向下移动
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            # 向下移动
            alien.rect.y += self.settings.fleet_drop_speed
        # 改变外星人移动方向
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到那样处理
                self._ship_hit()
                break

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整个外星舰队的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检查是否有外星人到达了屏幕的左下缘
        self._check_aliens_bottom()

    def _check_bullet_alien_collision(self):
        """响应子弹和外星人的碰撞"""
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            # 删除现有的子弹并创建一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # 提升等级
            self.stats.level +=1
            self.sb.prep_level()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        # 将ships_left减1
        if self.stats.ships_left >0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            # 创建一个新的外星舰队，并将其飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕（辅助方法）"""
        # 让最近绘制的屏幕可见，更新屏幕
        pygame.display.flip()
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        # 让外星人现身，
        self.aliens.draw(self.screen)
        # 显示得分
        self.sb.show_score()
        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()



if __name__ == '__main__':
    # 创建游戏并运行
    ai = AlienInvasion()
    ai.run_game()
