import pygame as pg
import random

# 自己的 library
import env
import block
import grass, carrot
import turtle, rabbit, fox

# 設定起始變數
random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有兔子物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
player_image = pg.transform.smoothscale(pg.image.load("images/ninja.png"), (55, 55))
flip_player_image = pg.transform.flip(player_image, True, False)
star_image = pg.transform.smoothscale(pg.image.load("images/star.png"), (15, 15))
rotate_star_images = []  # 讀取動畫圖片
for i in range(0, 20):
    rotate_star_images.append(pg.transform.rotate(star_image, 18 * i))

# 玩家
class PlayerSprite(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.xStep = 0
        self.yStep = 0
        self.face = "r"
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        group.add(self)

    def update(self):
        if self.face == "r":
            self.image = player_image
        elif self.face == "l":
            self.image = flip_player_image
        self.x += self.xStep
        self.y += self.yStep
        self.rect.center = [self.x, self.y]

    def move(self, direction):
        if direction == "u":
            self.yStep = -3
        if direction == "d":
            self.yStep = 3
        if direction == "r":
            self.xStep = 3
        if direction == "l":
            self.xStep = -3
        self.image = player_image
        self.face = direction

    def shoot(self):
        if self.face == "r":
            NinjaStarSprite(self.x, self.y, 15, 0)
        elif self.face == "l":
            NinjaStarSprite(self.x, self.y, -15, 0)
        elif self.face == "d":
            NinjaStarSprite(self.x, self.y, 0, 15)
        elif self.face == "u":
            NinjaStarSprite(self.x, self.y, 0, -15)

    def stop(self, direction):
        if direction == "x":
            self.xStep = 0
        if direction == "y":
            self.yStep = 0


# 飛鏢
class NinjaStarSprite(pg.sprite.Sprite):
    def __init__(self, x, y, xStep, yStep):  # x, y 為座標
        super().__init__()
        self.x = x
        self.y = y
        self.xStep = xStep
        self.yStep = yStep
        self.index = 0
        self.image = rotate_star_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        self.dead = False
        self.dead_index = 0
        group.add(self)

    def update(self):
        if self.dead:
            self.dead_index += 1
            if self.dead_index > 25:
                self.kill()
            return

        self.index += 1
        if self.index >= len(rotate_star_images):
            self.index = 0
        self.image = rotate_star_images[self.index]
        self.xStep *= 0.97
        self.yStep *= 0.97
        self.x += self.xStep
        self.y += self.yStep
        self.rect.center = [self.x, self.y]
        if (
            self.index > window_size[0]
            or self.index > window_size[1]
            or (abs(self.xStep) < 5 and abs(self.yStep) < 5)
        ):
            self.get_kill()

        for c in (
            pg.sprite.spritecollide(self, turtle.group, False)
            + pg.sprite.spritecollide(self, rabbit.group, False)
            + pg.sprite.spritecollide(self, fox.group, False)
        ):
            c.get_kill()
            self.get_kill()
            break

    def get_kill(self):
        self.dead = True


player_sprite = PlayerSprite(window_size[0] // 2, window_size[1] // 2)
