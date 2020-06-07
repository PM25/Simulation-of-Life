import pygame as pg
import random

# 自己的 library
import env
import block
import grass
import fox

random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有烏龜物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
walk_images = []  # 讀取動畫圖片
for i in range(1, 6):
    fname = f"images/animation/TURTLE/turtle{i}.png"
    walk_images.append(pg.transform.scale(pg.image.load(fname), (55, 55)))
flip_walk_images = []  # 讀取動畫圖片
for i in range(1, 6):
    flip_walk_images.append(pg.transform.flip(walk_images[i - 1], True, False))
eating_images = []
for i in range(1, 7):
    fname = f"images/animation/TURTLE/turtleeat{i}.png"
    eating_images.append(pg.transform.scale(pg.image.load(fname), (55, 55)))
flip_eating_images = []
for i in range(1, 7):
    fname = f"images/animation/TURTLE/turtleeat{i}.png"
    flip_eating_images.append(pg.transform.flip(eating_images[i - 1], True, False))
dead_image = pg.transform.scale(
    pg.image.load("images/animation/TURTLE/deadtrutle.png"), (55, 55)
)
dead_count = 0

# 烏龜
class TurtleSprite(pg.sprite.Sprite):
    def __init__(self, x, y):  # x, y 為座標
        super().__init__()
        self.index = 0
        self.image = walk_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.engery = 0
        self.x = x
        self.y = y
        self.xStep = random.randint(-1, 1)
        self.yStep = random.randint(-1, 1)
        self.eating = False
        self.eating_index = 0
        self.dead = False
        self.dead_index = 0
        group.add(self)

    def update(self):
        if self.dead:
            self.dead_index += 1
            if self.dead_index > 50:
                self.kill()
                global dead_count
                dead_count += 1
            return

        self.index += 0.3
        if self.eating and self.g.alive():
            self.eating_index += 1
            if self.index >= len(eating_images):
                self.index = 0
            if self.xStep < 0:
                self.image = eating_images[int(self.index)]
                self.xStep = -0.001
            else:
                self.image = flip_eating_images[int(self.index)]
                self.xStep = 0.001
            self.yStep = 0
            if self.eating_index > 80:
                self.g.kill()
                self.engery += 10
                if self.engery > 80:
                    self.birth(random.choice(["u", "d", "r", "l"]))
                    self.engery = 0
                self.eating = False
                self.eating_index = 0
                self.chase()
            self.run()
        else:
            if self.index >= len(walk_images):
                self.index = 0
            if self.xStep < 0:
                self.image = walk_images[int(self.index)]
            else:
                self.image = flip_walk_images[int(self.index)]
            r = random.random()
            if r < 0.01:
                self.xStep = random.randint(-1, 1)
                self.yStep = random.randint(-1, 1)
                self.chase()
            self.run()
            for g in pg.sprite.spritecollide(self, grass.group, False):
                self.g = g
                self.eating = True
                break
        if pg.sprite.spritecollideany(self, block.horiz_walls):
            self.yStep = -self.yStep
            self.xStep = random.randint(-1, 1)
        if pg.sprite.spritecollideany(self, block.vert_walls):
            self.xStep = -self.xStep
            self.yStep = random.randint(-1, 1)
        self.x += self.xStep / 2
        self.y += self.yStep / 2
        if self.x <= 30:
            self.x = 30
            self.xStep = random.randint(0, 1)
        if self.y <= 30:
            self.y = 30
            self.yStep = random.randint(0, 1)
        if self.x >= window_size[0] - 30:
            self.x = window_size[0] - 30
            self.xStep = random.randint(-1, 0)
        if self.y >= window_size[1] - 30:
            self.y = window_size[1] - 30
            self.yStep = random.randint(-1, 0)
        self.rect.center = [self.x, self.y]

    def birth(self, direction):
        if direction == "u":
            turtle = TurtleSprite(self.x, self.y - 25)
        if direction == "d":
            turtle = TurtleSprite(self.x, self.y + 25)
        if direction == "r":
            turtle = TurtleSprite(self.x - 25, self.y)
        if direction == "l":
            turtle = TurtleSprite(self.x + 25, self.y)

    def get_kill(self):
        self.image = dead_image
        self.dead = True

    def chase(self):
        pos = pg.math.Vector2(self.x, self.y)
        if len(grass.group) > 0:
            g = min(
                [g for g in grass.group],
                key=lambda g: pos.distance_to(pg.math.Vector2(g.a, g.b)),
            )
            distance = pos.distance_to(pg.math.Vector2(g.a, g.b))

            if distance < 100:
                if g.a > self.x:
                    self.xStep = 1
                else:
                    self.xStep = -1

                if g.b > self.y:
                    self.yStep = 1
                else:
                    self.yStep = -1
            else:
                self.xStep = random.randint(-1, 1)
                self.yStep = random.randint(-1, 1)
        else:
            self.xStep = random.randint(-1, 1)
            self.yStep = random.randint(-1, 1)

    def run(self):
        pos = pg.math.Vector2(self.x, self.y)
        if len(fox.group) > 0:
            f = min(
                [f for f in fox.group],
                key=lambda f: pos.distance_to(pg.math.Vector2(f.x, f.y)),
            )
            distance = pos.distance_to(pg.math.Vector2(f.x, f.y))

            if distance < 75:
                self.eating = False
                if f.x > self.x:
                    self.xStep = -1
                else:
                    self.xStep = 1

                if f.y > self.y:
                    self.yStep = -1
                else:
                    self.yStep = 1
