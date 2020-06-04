import random
import pygame as pg


# 自己的 library
import env
import block
import carrot

# 設定起始變數
random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有草物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
image = pg.transform.scale(pg.image.load("images/grass.png"), (25, 25))  # 讀取草圖片


# 草
class GrassSprite(pg.sprite.Sprite):
    def __init__(self, x, y):  # x, y 為座標
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.day = 0
        self.a = x
        self.b = y
        self.check()

    def check(self):
        co = pg.sprite.spritecollideany(self, group)
        co1 = pg.sprite.spritecollideany(self, block.group)
        co2 = pg.sprite.spritecollideany(self, carrot.group)
        if co == None and co1 == None and co2 == None:
            group.add(self)

    def birth(self, direction):
        if direction == "u":
            self.b -= 25
        if direction == "d":
            self.b += 25
        if direction == "r":
            self.a -= 25
        if direction == "l":
            self.a += 25
        grass = GrassSprite(self.a, self.b)

    def update(self):
        self.day += 1
        if self.day == 365:
            self.day = random.randint(0, 364)
            self.birth(random.choice(["u", "d", "l", "r"]))