import pygame as pg
import random

# 自己的 library
import env
import block
import grass

random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有烏龜物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
walk_images = []  # 讀取動畫圖片
for i in range(1, 6):
    fname = f"images/animation/TURTLE/turtle{i}.png"
    walk_images.append(pg.transform.scale(pg.image.load(fname), (30, 30)))
flip_walk_images = []  # 讀取動畫圖片
for i in range(1, 6):
    flip_walk_images.append(pg.transform.flip(walk_images[i - 1], True, False))
eating_images = []
for i in range(1, 7):
    fname = f"images/animation/TURTLE/turtleeat{i}.png"
    eating_images.append(pg.transform.scale(pg.image.load(fname), (30, 30)))
flip_eating_images = []
for i in range(1, 7):
    fname = f"images/animation/TURTLE/turtleeat{i}.png"
    flip_eating_images.append(pg.transform.flip(eating_images[i - 1], True, False))

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
        group.add(self)

    def update(self):
        self.index += 0.5
        if self.eating:
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
                self.eating = False
                self.eating_index = 0
                self.chase()
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
            for g in pg.sprite.spritecollide(self, grass.group, False):
                g.kill()
                self.eating = True
                self.engery += 10
                if self.engery > 100:
                    self.birth(random.choice(["u", "d", "r", "l"]))
                    self.engery = 0
                break
        if pg.sprite.spritecollideany(self, block.horiz_walls):
            self.yStep = -self.yStep
            self.xStep = random.randint(-1, 1)
        if pg.sprite.spritecollideany(self, block.vert_walls):
            self.xStep = -self.xStep
            self.yStep = random.randint(-1, 1)
        self.x += self.xStep
        self.y += self.yStep
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


# 程式從這裡開始
if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("迷你生態圈")  # 標題
    screen = pg.display.set_mode(window_size)
    bg_image = pg.image.load("images/background.png")  # 背景圖片
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 1000)

    # 隨機產生 25株草
    for i in range(25):
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        grass.GrassSprite(x, y)  # 在 x, y 座標創建一株草

    # 隨機產生 3隻烏龜
    for i in range(10):
        x = random.randint(30, window_size[0] - 50)  # x座標
        y = random.randint(30, window_size[1] - 50)  # y座標
        TurtleSprite(x, y)  # 在 x, y 座標創建一隻烏龜

    # 把所有物件集合起來
    sprites = pg.sprite.OrderedUpdates(grass.group, group)

    # 遊戲迴圈
    done = False
    while not done:
        clock.tick(FPS)  # 設定 FPS
        screen.blit(bg_image, [0, 0])  # 畫遊戲背景
        sprites.update()  # 執行所有 TurtleSprite, GrassSprite 裡面的 Update()
        sprites.draw(screen)  # 畫出所有 TurtleSprite, GrassSprite 到遊戲上
        pg.display.update()  # 更新畫面

        # 當有事件發生時 (例: 滑鼠、鍵盤)
        for event in pg.event.get():
            # 按下結束按鍵時
            if event.type == pg.QUIT:
                done = True  # 遊戲結束
            if event.type == pg.USEREVENT:
                sprites = pg.sprite.OrderedUpdates(grass.group, group)
                # 若超過 550 隻烏龜的話結束遊戲
                if len(group) > 550:
                    Done = True
                # 顯示有多少烏龜在畫面上
                print(f"現在畫面上有 {len(group)} 隻烏龜")
    pg.quit()  # 結束遊戲
