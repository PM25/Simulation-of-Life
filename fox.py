import pygame as pg
import random

# 自己的 library
import env
import block
import grass, carrot
import turtle, rabbit, player

# 設定起始變數
random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有狐狸物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
walk_images = []  # 讀取動畫圖片
for i in range(1, 10):
    fname = f"images/animation/FOX/fox{i}.png"
    walk_images.append(pg.transform.smoothscale(pg.image.load(fname), (55, 55)))

eat_images = []  # 讀取動畫圖片
for i in range(1, 6):
    fname = f"images/animation/FOX/foxeat{i}.png"
    eat_images.append(pg.transform.smoothscale(pg.image.load(fname), (55, 55)))

dead_image = pg.transform.smoothscale(
    pg.image.load("images/animation/FOX/daed fox.png"), (55, 55)
)
dead_count = 0

# 狐狸
class FoxSprite(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.index = 0
        self.x = x
        self.y = y
        self.xStep = random.randint(-3, 3)
        self.yStep = random.randint(-3, 3)
        self.image = walk_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.eating = False
        self.eating_index = 0
        self.dead = False
        self.dead_index = 0
        self.run_index = 0
        group.add(self)

    def update(self):
        if self.dead:
            self.dead_index += 1
            if self.dead_index > 50:
                self.kill()
                global dead_count
                dead_count += 1
            return

        self.index += 0.5
        if self.eating and self.t.alive() and self.run_index == 0:
            self.eating_index += 1
            if self.index >= len(eat_images):
                self.index = 0
            self.image = eat_images[int(self.index)]
            self.xStep = 0
            self.yStep = 0

            if self.eating_index >= 50:
                self.eating = False
                self.eating_index = 0
                self.chase()
            self.run()

        else:
            if self.index >= len(walk_images):
                self.index = 0
            self.image = walk_images[int(self.index)]

            R = random.random()
            if R < 0.05:
                self.xStep = random.randint(-3, 3)
                self.yStep = random.randint(-3, 3)
                self.chase()
            self.run()
            if self.run_index > 0:
                self.run_index -= 1
            else:
                for c in pg.sprite.spritecollide(
                    self, turtle.group, False
                ) + pg.sprite.spritecollide(self, rabbit.group, False):
                    self.t = c
                    self.t.get_kill()
                    self.eating = True
                    break

        if pg.sprite.spritecollideany(self, block.horiz_walls):
            self.yStep = -self.yStep
            self.xStep = random.randint(-3, 3)
        if pg.sprite.spritecollideany(self, block.vert_walls):
            self.xStep = -self.xStep
            self.yStep = random.randint(-3, 3)
        self.x += self.xStep
        self.y += self.yStep

        if self.x <= 30:
            self.x = 30
            self.xStep = random.randint(0, 2)
        if self.y <= 30:
            self.y = 30
            self.yStep = random.randint(0, 2)
        if self.x >= window_size[0] - 30:
            self.x = window_size[0] - 30
            self.xStep = random.randint(-2, 0)
        if self.y >= window_size[1] - 30:
            self.y = window_size[1] - 30
            self.yStep = random.randint(-2, 0)
        self.rect.center = [self.x, self.y]

    def birth(self, direction):
        if direction == "u":
            fox = FoxSprite(self.x, self.y - 30)
        if direction == "d":
            fox = FoxSprite(self.x, self.y + 30)
        if direction == "r":
            fox = FoxSprite(self.x + 30, self.y)
        if direction == "l":
            fox = FoxSprite(self.x - 30, self.y)

    def get_kill(self):
        self.image = dead_image
        self.dead = True

    def chase(self):
        pos = pg.math.Vector2(self.x, self.y)
        if len(turtle.group) > 0 or len(rabbit.group) > 0:
            c = min(
                [t for t in turtle.group] + [r for r in rabbit.group],
                key=lambda c: pos.distance_to(pg.math.Vector2(c.x, c.y)),
            )
            distance = pos.distance_to(pg.math.Vector2(c.x, c.y))
            if distance < 100:
                if c.x > self.x:
                    self.xStep = 2
                else:
                    self.xStep = -2

                if c.y > self.y:
                    self.yStep = 2
                else:
                    self.yStep = -2

    def run(self):
        pos = pg.math.Vector2(self.x, self.y)
        p = min(
            [p for p in player.group],
            key=lambda p: pos.distance_to(pg.math.Vector2(p.x, p.y)),
        )
        distance = pos.distance_to(pg.math.Vector2(p.x, p.y))
        if distance < 120:
            self.eating = False
            self.run_index = 30
            if player.player_sprite.x > self.x:
                self.xStep = -3.5
            else:
                self.xStep = 3.5

            if player.player_sprite.y > self.y:
                self.yStep = -3.5
            else:
                self.yStep = 3.5
