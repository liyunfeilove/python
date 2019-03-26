"""
飞机大战
"""

import sys
import random
import pygame
import pygame.locals

BACKGROUND = pygame.image.load("res/img_bg_level_2.jpg")
GAME_ICO = pygame.image.load("res/hero3.png")
PLAY_IMG = pygame.image.load("res/hero2.png")
ENEMY_IMG = [("res/img-plane_" + str(n) + ".png") for n in range(1, 8)]
BULLET_IMG = pygame.image.load("res/bullet_14.png")
BOMB_IMG = [pygame.image.load("res/eff" + str(n) + ".png") for n in range(1, 5)]


class Modle():
    window = None

    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y

    def show(self):
        self.window.blit(self.img, (self.x, self.y))

    @staticmethod
    def rect(rect1, rect2):
        return pygame.Rect.colliderect(rect1, rect2)


class Background(Modle):
    def move(self):
        if self.y < Main.SIZE_HIGH:
            self.y += 1
        else:
            self.y = 0

    def show(self):
        super().show()
        self.window.blit(self.img, (self.x, self.y - Main.SIZE_HIGH))


class Play_plan(Modle):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.bullets = []

    def show(self, enemys):
        super().show()
        remove_list = []
        for bullet in self.bullets:
            if bullet.y < -56:
                remove_list.append(bullet)
            else:
                rect_bullet = pygame.locals.Rect(bullet.x, bullet.y, 20, 56)
                for enemy in enemys:  # TODO 子弹与敌机碰撞检测
                    rect_enemy = pygame.locals.Rect(enemy.x, enemy.y, 100, 68)
                    if Modle.rect(rect_bullet, rect_enemy):
                        remove_list.append(bullet)
                        enemy.is_hit = True
                        enemy.bomb.is_show = True
                        enemy.bomb.x = enemy.x
                        enemy.bomb.y = enemy.y
                        sound = pygame.mixer.Sound("res/bomb.wav")
                        sound.play()
                        break

        for bullet in remove_list:
            self.bullets.remove(bullet)
        play_rect = pygame.locals.Rect(self.x, self.y, 120, 78)
        for enemy in enemys:  # TODO 玩家与敌机碰撞检测
            rect_enemy = pygame.locals.Rect(enemy.x, enemy.y, 100, 68)
            if Modle.rect(play_rect, rect_enemy):
                enemy.is_hit = True
                pygame.mixer.music.load("res/gameover.wav")
                pygame.mixer.music.play(loops=1)
                return 2  # 2表示游戏结束
        return 1  # 表示游戏正在进行中


class Enemy_plan(Modle):
    def __init__(self):
        self.x = random.randint(0, Main.SIZE_WIDE - 100)
        self.y = random.randint(-Main.SIZE_HIGH, - 68)
        self.img = pygame.image.load(ENEMY_IMG[random.randint(0, 6)])
        self.is_hit = False
        self.bomb = Bomb()

    def move(self):
        if self.y < Main.SIZE_HIGH and not self.is_hit:
            self.y += 3
        else:
            self.x = random.randint(0, Main.SIZE_WIDE - 100)
            self.y = random.randint(-Main.SIZE_HIGH, - 68)
            self.is_hit = False

    def show(self):
        super().show()
        if self.bomb.is_show:  # 如果是爆破展示时间，则调用爆破显示方法
            self.bomb.show()


class Bullet(Modle):
    def move(self):
        self.y -= 10


# TODO 爆破特效
class Bomb(Modle):
    def __init__(self):
        self.x = None
        self.y = None
        self.imgs = BOMB_IMG  # 爆炸图片列表
        self.is_show = False  # 设置爆破特效开关
        self.time = 0  # 设置控制爆破时间的变量

    def show(self):
        if self.is_show and self.time < len(self.imgs) * 3:
            self.window.blit(self.imgs[self.time // 3], (self.x, self.y))
            self.time += 1
        else:
            self.is_show = False
            self.time = 0


class Main():
    SIZE_WIDE = 512
    SIZE_HIGH = 768

    def __init__(self):
        self.state = 0  # 0未开始，1正在进行中，2，游戏中死亡

    def run(self):
        pygame.init()
        pygame.mixer.init()

        self.modle_init()

        pygame.mixer.music.load("res/bg.wav")
        pygame.mixer.music.play()

        while True:
            self.background.show()
            self.background.move()
            if self.state == 0:  # 游戏未开始显示主界面
                self.show_init()
            elif self.state == 1:  # 游戏开始
                for enemy in self.enemys:
                    enemy.move()
                    enemy.show()
                self.state = self.play.show(self.enemys)
                for bullet in self.play.bullets:
                    bullet.move()
                    bullet.show()
            elif self.state == 2:  # 游戏中死亡
                font_over = pygame.font.Font("res/DENGB.TTF", 60)
                text_obj = font_over.render("GAME OVER！", 1, (255, 0, 0))
                self.window.blit(text_obj,
                                 pygame.locals.Rect(self.SIZE_WIDE / 2 - 300 / 2, self.SIZE_HIGH / 2 - 100 / 2, 300,
                                                    100))
                self.enemys = []
                self.state = 0

            pygame.display.update()
            self.event_init()

    def show_init(self):
        font_over = pygame.font.Font("res/DENGB.TTF", 50)
        text_obj = font_over.render("飞机大战荣耀版", 1, (0, 0, 0))
        self.window.blit(text_obj,
                         pygame.locals.Rect(self.SIZE_WIDE / 2 - 180, self.SIZE_HIGH / 2 - 50 / 2, 260, 50))

        font_over = pygame.font.Font("res/DENGB.TTF", 40)
        text_obj = font_over.render("【1】 简单", 1, (255, 0, 0))
        self.window.blit(text_obj,
                         pygame.locals.Rect(self.SIZE_WIDE / 2 - 260 / 2, self.SIZE_HIGH / 2 - 50 / 2 + 60, 260, 50))

        font_over = pygame.font.Font("res/DENGB.TTF", 40)
        text_obj = font_over.render("【2】 困难", 1, (0, 255, 0))
        self.window.blit(text_obj,
                         pygame.locals.Rect(self.SIZE_WIDE / 2 - 260 / 2, self.SIZE_HIGH / 2 - 50 / 2 + 120, 260, 50))

    def modle_init(self):
        self.window = pygame.display.set_mode((self.SIZE_WIDE, self.SIZE_HIGH))
        Modle.window = self.window
        pygame.display.set_icon(GAME_ICO)
        pygame.display.set_caption("飞机大战荣耀版")

        self.background = Background(BACKGROUND, 0, 0)
        self.play = Play_plan(PLAY_IMG, 200, 300)
        self.enemys = []

    def event_init(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit()
            if event.type == pygame.locals.MOUSEMOTION and self.state == 1:
                x, y = pygame.mouse.get_pos()
                self.play.x = x - 120 / 2
                self.play.y = y - 78 / 2
            if self.state == 0 or self.state == 2:
                if event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_1:
                    for i in range(25):
                        self.enemys.append(Enemy_plan())
                    self.state = 1
                elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_2:
                    for i in range(100):
                        self.enemys.append(Enemy_plan())
                    self.state = 1
            if pygame.mouse.get_pressed()[0] == 1 and self.state == 1:
                x = self.play.x + 120 / 2 - 20 / 2
                y = self.play.y - 56
                self.play.bullets.append(Bullet(BULLET_IMG, x, y))


if __name__ == '__main__':
    game = Main()
    game.run()
