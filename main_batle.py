"""
飞机大战
"""
import sys
import random
import pygame
import pygame.locals  # 导入pygame本地设置的资源，包含程序执行过程中所使用的各种常量，例如键盘按钮，鼠标按钮等

BACKGROUND_IMG = ("res/img_bg_level_2.png", "res/img_bg_level_1.png")
GAME_ICON = pygame.image.load("res/game.ico")
PLAYER_IMG = pygame.image.load("res/hero3.png")
ENEMY_IMGS = (
    "res/img-plane_1.png", "res/img-plane_2.png", "res/img-plane_3.png", "res/img-plane_4.png", "res/img-plane_5.png",
    "res/img-plane_6.png", "res/img-plane_7.png")
BULLET_IMG1 = pygame.image.load("res/bullet_12.png")
BULLET_IMG2 = pygame.image.load("res/bullet_10.png")
BOMB_IGM = [pygame.image.load("res/eff" + str(i) + ".png") for i in range(1, 5)]


# TODO 定义窗体模型，并将其他对象插入到模型中

class ModelWindow:  # 主窗口模型，用于初始化其内部对象和显示对象
    window = None  # 主窗口对象

    def __init__(self, image, x, y):
        self.image = image  # 图片
        self.x = x  # x坐标
        self.y = y  # y坐标

    def show(self):
        self.window.blit(self.image, (self.x, self.y))  # 将对象添加到主窗口中显示

    @staticmethod
    def is_hit(rect1, rect2):  # 创建两个对象碰撞结果的检测方法
        return pygame.Rect.colliderect(rect1, rect2)  # 返回碰撞结果，结果为bool


# TODO 背景类
class Background(ModelWindow):
    images = []  # 背景图片列表

    def __init__(self, x, y):
        for i in range(2):  # 重写初始化方法，自定义背景图片
            self.images.append(pygame.image.load(BACKGROUND_IMG[i]))
        super().__init__(self.images[random.randint(0, 1)], x, y)  # 调用父类方法

    def move(self):  # 背景移动
        if self.y <= Game.SIZE_HEIGHT:
            self.y += 3
        else:
            self.y = 0

    def show(self):
        super().show()  # 调用被重写的父类的方法，显示主背景图片
        self.window.blit(self.image, (self.x, self.y - Game.SIZE_HEIGHT))  # 显示辅助背景图片


# TODO 玩家类
class PlayerPlane(ModelWindow):
    def __init__(self, image, x, y):  # 重写初始化方法，增加玩家的子弹对象
        super().__init__(image, x, y)  # 调用父类方法
        self.bullet1 = []
        self.bullet2 = []
        self.bullet3 = []

    def show(self, enemys):  # 重写显示方法，传入敌机对象做碰撞检测
        self.window.blit(self.image, (self.x, self.y))  # 飞机显示
        remove_list = []  # 优化子弹，如果子弹超出屏幕则删除子弹对象
        for bullet in self.bullet1:  # 循环子弹
            if bullet.y < -60:
                remove_list.append(bullet)  # 跑出屏幕就加入删除列表
            else:  # 如果在屏幕内，创建子弹矩阵对象
                bullet_rect = pygame.locals.Rect(bullet.x, bullet.y, 20, 29)
                for enemy in enemys:  # 创建敌机矩阵对象
                    enemy_rect = pygame.locals.Rect(enemy.x, enemy.y, 100, 68)
                    if ModelWindow.is_hit(bullet_rect, enemy_rect):  # 判断子弹和敌机是否相撞
                        enemy.is_hited = True  # 相撞后设置敌机已被击中
                        enemy.bomb.show_time = True  # 相撞后设置爆破效果为可以开启
                        enemy.bomb.x = enemy.x  # 设置爆破开始的x坐标
                        enemy.bomb.y = enemy.y  # 设置爆破开始y的坐标
                        sound = pygame.mixer.Sound("res/bomb.wav")  # 添加混音音效文件
                        sound.play()  # 播放爆破效果音
                        game.game_score += 1  # 分数加一
                        remove_list.append(bullet)  # 删除与敌机碰撞的子弹
                        break  # 一个子弹和一个敌机相撞后，停止检查其他敌机，检查下一颗子弹
        for bullet in remove_list:  # 删除跑出屏幕的子弹
            self.bullet1.remove(bullet)  # 从原始子弹列表中删除要删除的子弹

        rect_play = pygame.locals.Rect(self.x, self.y, 200, 206)  # 创建玩家矩阵对象
        for enemy in enemys:
            enemy_rect = pygame.locals.Rect(enemy.x, enemy.y, 100, 68)  # 创建敌机矩阵对象
            if ModelWindow.is_hit(rect_play, enemy_rect):  # 玩家与敌机的碰撞检测
                enemy.is_hited = True  # 相撞后标记敌机已被摧毁
                pygame.mixer.music.load("res/gameover.wav")  # 加载游戏背景音乐文件为游戏结束
                pygame.mixer.music.play(loops=1)  # 播放背景音乐  loops=1 控制播放次数
                return 2  # 设置当前操作返回2,表示游戏结束
        return 1  # 设置正常操作状态下返回True，表示游戏进行中


# TODO 子弹类
class Bullet(ModelWindow):
    def move(self):  # 子弹移动方法
        self.y -= 25


# TODO 添加爆破效果类
class Bomb(ModelWindow):
    def __init__(self):
        self.images = BOMB_IGM  # 添加爆破效果图片列表
        self.show_time = False  # 添加是否开启爆破效果判断
        self.times = 0  # 定义爆破图片展示控制变量

    def show(self):  # 重写显示方法
        if self.show_time and self.times < len(self.images) * 2:  # 判断是否是显示时间和爆炸效果超出范围
            self.window.blit(self.images[self.times // 2], (self.x, self.y))  # 延长播放次数，放大循环次数，拉长播放时间
            self.times += 1  # 控制变量每次+1
        else:  # 控制爆破展示完毕后恢复状态
            self.times = 0  # 控制爆破展示完毕后恢复后下次展示图片从第一个开始
            self.show_time = False  # 控制爆破展示完毕后恢复后设置为不开始爆炸效果


# TODO 敌机类
class EnemyPlane(ModelWindow):
    def __init__(self):  # 自定义敌机属性
        self.image = pygame.image.load(ENEMY_IMGS[random.randint(0, 6)])  # 随机图片
        self.x = random.randint(0, Game.SIZA_WIDTH - 100)  # x范围坐标
        self.y = random.randint(-Game.SIZE_HEIGHT, -68)  # y范围坐标
        self.is_hited = False  # 添加敌机是否被击中判断
        self.bomb = Bomb()  # 为敌机添加绑定的爆破效果

    def move(self):
        if self.y > Game.SIZE_HEIGHT or self.is_hited:  # 判断敌机是否被击中或跑出屏幕
            self.image = pygame.image.load(ENEMY_IMGS[random.randint(0, 6)])  # 随机图片
            self.x = random.randint(0, Game.SIZA_WIDTH - 100)  # 重新初始化x坐标
            self.y = random.randint(-Game.SIZE_HEIGHT, -68)  # 重新初始化y坐标
            self.is_hited = False  # 重置状态为未击中
        else:
            self.y += 10

    def show(self):  # 重写显示方法
        super().show()  # 调用父类方法
        if self.bomb.show_time == True:  # 如果开启爆破效果
            self.bomb.show()  # 调用爆破对象的显示方法


# TODO 游戏类，主程序入口
class Game:
    SIZA_WIDTH = 765
    SIZE_HEIGHT = 989

    #  定义构造方法
    def __init__(self):
        self.game_begin = 0  # 判断游戏状态，0未开始，1正在游戏，2游戏结束
        self.game_score = 0  # 记录游戏分数

    # TODO 主程序入口
    def run(self):
        pygame.init()  # 初始化pygame读取系统操作
        self.window_init()  # 创建主窗口

        pygame.mixer.init()  # 初始化背景音乐模块
        pygame.mixer.music.load("res/bg.wav")  # 加载背景音乐文件
        pygame.mixer.music.play()  # 播放背景音乐

        self.model_init()  # 创建窗体对象初始化
        while True:
            self.background.move()  # 背景移动
            self.background.show()  # 移动完毕后将背景插入窗口中

            if self.game_begin == 0:  # 游戏未开始显示主界面
                font_over = pygame.font.Font("res/DENGB.TTF", 60)  # TODO  设置大字体
                text_over = font_over.render("二次元乱入飞机大战", 1, (255, 255, 0))  # TODO  设置文字
                self.window.blit(text_over, pygame.locals.Rect(115, 400, 360, 60))  # TODO  设置显示位置

                font_over = pygame.font.Font("res/DENGB.TTF", 40)  # TODO  设置小字体
                text_over = font_over.render("请选择难度", 1, (255, 255, 255))
                self.window.blit(text_over, pygame.locals.Rect(265, 550, 360, 60))

                font_over = pygame.font.Font("res/DENGB.TTF", 50)  # TODO  设置中字体
                text_over = font_over.render("1-初入江湖", 1, (0, 255, 0))
                self.window.blit(text_over, pygame.locals.Rect(265, 600, 360, 60))

                text_over = font_over.render("2-小试牛刀", 1, (255, 255, 255))
                self.window.blit(text_over, pygame.locals.Rect(265, 700, 360, 60))

                text_over = font_over.render("3-恶魔地狱", 1, (255, 0, 0))
                self.window.blit(text_over, pygame.locals.Rect(265, 800, 360, 60))
            elif self.game_begin == 1:  # 游戏开始，添加玩家，敌机，子弹等模型并显示
                self.game_begin = self.play.show(self.enemys)  # 加入玩家飞机，并接收游戏状态
                for enemy in self.enemys:  # 敌机移动和显示
                    enemy.move()
                    enemy.show()
                for bullet in self.play.bullet1:  # 循环子弹
                    bullet.move()  # 子弹移动
                    bullet.show()  # 直接调用显示方法
                for bullet in self.play.bullet2:
                    bullet.move()
                    bullet.show()
                for bullet in self.play.bullet3:
                    bullet.move()
                    bullet.show()

                font_over = pygame.font.Font("res/DENGB.TTF", 50)  # TODO  显示分数
                text_over = font_over.render("分数：%d" % self.game_score, 1, (0, 255, 0))
                self.window.blit(text_over, pygame.locals.Rect(450, 100, 200, 60))

            elif self.game_begin == 2:  # 游戏中死亡
                font_over = pygame.font.Font("res/DENGB.TTF", 60)  # 创建字体对象
                text_obj = font_over.render("GAME OVER", 1, (255, 0, 0))  # 创建文本对象
                self.window.blit(text_obj, pygame.locals.Rect(265, 500, 360, 60))  # 添加文本对象到屏幕上
                self.enemys = []  # 重置敌机为0
                self.game_score = 0  # 重置分数为0
                self.game_begin = 0  # 重返主界面

            self.event_init()  # 监听窗体事件，判断事件并执行
            pygame.display.update()  # 刷新主窗体

    def window_init(self):  # 初始化窗口
        self.window = pygame.display.set_mode((Game.SIZA_WIDTH, Game.SIZE_HEIGHT))  # 创建主窗体
        ModelWindow.window = self.window  # 将创建好的主窗口赋值给Modl1使用
        pygame.display.set_icon(GAME_ICON)  # 游戏图标
        pygame.display.set_caption("二次元乱入飞机大战")  # 游戏名称

    def model_init(self):  # 初始化窗口里面的对象
        self.background = Background(0, 0)  # 定义背景对象
        self.play = PlayerPlane(PLAYER_IMG, 350, 500)  # 定义玩家对象
        self.enemys = []  # 定义敌机对象列表

    def event_init(self):  # 监听窗口事件
        for event in pygame.event.get():  # 获取窗口事件列表，遍历判断
            if event.type == pygame.locals.QUIT:  # 如果点击x则退出系统
                sys.exit()

            elif event.type == pygame.locals.MOUSEMOTION and self.game_begin == 1:  # 捕捉鼠标位置
                pos = pygame.mouse.get_pos()  # 玩家获取到鼠标信息，保持与鼠标一致
                self.play.x = pos[0] - 100
                self.play.y = pos[1] - 150

            elif event.type == pygame.locals.KEYDOWN:  # 捕捉键盘事件
                if self.game_begin == 0 or self.game_begin == 2:  # 游戏未开始,主界面按键捕捉
                    if event.key == pygame.locals.K_1:
                        for _ in range(30):
                            self.enemys.append(EnemyPlane())
                        self.game_begin = 1
                    elif event.key == pygame.locals.K_2:
                        for _ in range(50):
                            self.enemys.append(EnemyPlane())
                        self.game_begin = 1
                    elif event.key == pygame.locals.K_3:
                        for _ in range(100):
                            self.enemys.append(EnemyPlane())
                            self.game_begin = 1
                elif self.game_begin == 1:  # 游戏中有按键操作
                    if event.key == pygame.locals.K_SPACE:  # 按下空格，炸毁所有敌机
                        for enemy in self.enemys:
                            enemy.is_hited = True  # 标记所有敌机被击毁
                            enemy.bomb.show_time = True  # 爆破效果同时开启
                            enemy.bomb.x = enemy.x
                            enemy.bomb.y = enemy.y
                            self.game_score += 1  # 分数加1
                            sound = pygame.mixer.Sound("res/bomb.wav")
                            sound.play()  # 播放爆破效果音

            if self.game_begin == 1:  # 游戏开始后获取鼠标状态
                mouse_state = pygame.mouse.get_pressed()  # 获取鼠标左键状态，返回元组，保存鼠标左中右按键状态
                if mouse_state[0] == 1:  # 判断左键是否按下
                    pos = pygame.mouse.get_pos()  # 获取鼠标位置
                    # 设置三种子弹位置，并且发射子弹
                    self.play.bullet1.append(Bullet(BULLET_IMG1, pos[0] - 10, pos[1] - 160))
                    self.play.bullet2.append(Bullet(BULLET_IMG2, pos[0] - 50, pos[1] - 180))
                    self.play.bullet3.append(Bullet(BULLET_IMG2, pos[0] + 30, pos[1] - 180))


if __name__ == '__main__':
    game = Game()
    game.run()
