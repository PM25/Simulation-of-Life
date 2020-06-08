import pygame as pg
import random

# 自己的 library
import env
import block
import grass

# 設定起始變數
random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有紅蘿蔔物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
image = pg.transform.scale(pg.image.load("images/carrots.png"), (25, 25))  # 讀取紅蘿蔔圖片


# 紅蘿蔔
class CarrotSprite(pg.sprite.Sprite):
    def __init__(self, x, y):  # x, y 為座標
        super().__init__()
        self.x = x
        self.y = y
        self.day = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.check()

    def update(self):
        self.day += 1
        if self.day == 365:
            self.day = random.randint(0, 364)
            self.birth(random.choice(["u", "d", "r", "l"]))

    def birth(self, direction):
        if direction == "u":
            self.y -= 25
        elif direction == "d":
            self.y += 25
        elif direction == "r":
            self.x += 25
        elif direction == "l":
            self.x -= 25
        carrot = CarrotSprite(self.x, self.y)

    def check(self):
        co = pg.sprite.spritecollideany(self, group)
        co1 = pg.sprite.spritecollideany(self, block.group)
        co2 = pg.sprite.spritecollideany(self, grass.group)
        if (
            co == None
            and co1 == None
            and co2 == None
            and self.x > 0
            and self.x < window_size[0]
            and self.y > 0
            and self.y < window_size[1]
        ):
            group.add(self)
