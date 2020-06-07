import pygame as pg
import random

# 自己的 library
import env
import block
import carrot
import fox

random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有兔子物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
walk_images = []  # 讀取動畫圖片
for i in range(1, 17):
    fname = f"images/animation/RABBIT/rabbit{i}.png"
    walk_images.append(pg.transform.scale(pg.image.load(fname), (40, 40)))
flip_walk_images = []  # 讀取動畫圖片
for i in range(1, 17):
    flip_walk_images.append(pg.transform.flip(walk_images[i - 1], True, False))
eating_images = []
for i in range(1, 17):
    fname = f"images/animation/RABBIT/rabbiteat{i}.png"
    eating_images.append(pg.transform.scale(pg.image.load(fname), (40, 40)))
flip_eating_images = []
for i in range(1, 17):
    flip_eating_images.append(pg.transform.flip(eating_images[i - 1], True, False))
dead_image = pg.transform.scale(
    pg.image.load("images/animation/RABBIT/deadrabbit.png"), (40, 40)
)


# 兔子
class RabbitSprite(pg.sprite.Sprite):
    def __init__(self, x, y):  # x, y 為座標
        super().__init__()
        self.index = 0
        self.x = x
        self.y = y
        self.energy = 0
        self.xStep = random.randint(-2, 2)
        self.yStep = random.randint(-2, 2)
        self.image = walk_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
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
            return

        self.index += 1
        if self.eating and self.c.alive():
            self.eating_index += 1
            if self.index >= len(eating_images):
                self.index = 0
            if self.xStep > 0:
                self.image = eating_images[self.index]
                self.xStep = 0.001
            else:
                self.image = flip_eating_images[self.index]
                self.xStep = -0.001
            self.yStep = 0

            if self.eating_index > 70:
                self.c.kill()
                self.energy += 10
                if self.energy > 80:
                    self.birth(random.choice(["u", "d", "r", "l"]))
                    self.energy = 0
                self.eating = False
                self.eating_index = 0
                self.chase()
            self.run()
        else:
            if self.index >= len(walk_images):
                self.index = 0
            if self.xStep > 0:
                self.image = walk_images[self.index]
            else:
                self.image = flip_walk_images[self.index]

            r = random.random()
            if r < 0.025:
                self.xStep = random.randint(-2, 2)
                self.yStep = random.randint(-2, 2)
                self.chase()
            self.run()

            for c in pg.sprite.spritecollide(self, carrot.group, False):
                self.c = c
                self.eating = True
                break
        if pg.sprite.spritecollideany(self, block.horiz_walls):
            self.yStep = -self.yStep
            self.xStep = random.randint(-2, 2)
        if pg.sprite.spritecollideany(self, block.vert_walls):
            self.xStep = -self.xStep
            self.yStep = random.randint(-2, 2)
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
            rabbit = RabbitSprite(self.x, self.y - 25)
        if direction == "d":
            rabbit = RabbitSprite(self.x, self.y + 25)
        if direction == "r":
            rabbit = RabbitSprite(self.x + 25, self.y)
        if direction == "l":
            rabbit = RabbitSprite(self.x - 25, self.y)

    def get_kill(self):
        self.image = dead_image
        self.dead = True

    def chase(self):
        pos = pg.math.Vector2(self.x, self.y)
        if len(carrot.group) > 0:
            c = min(
                [c for c in carrot.group],
                key=lambda c: pos.distance_to(pg.math.Vector2(c.x, c.y)),
            )
            distance = pos.distance_to(pg.math.Vector2(c.x, c.y))
            if distance < 120:
                if c.x > self.x:
                    self.xStep = 1.5
                else:
                    self.xStep = -1.5

                if c.y > self.y:
                    self.yStep = 1.5
                else:
                    self.yStep = -1.5
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

            if distance < 100:
                self.eating = False
                if f.x > self.x:
                    self.xStep = -2.5
                else:
                    self.xStep = 2.5

                if f.y > self.y:
                    self.yStep = -2.5
                else:
                    self.yStep = 2.5


# 程式從這裡開始
if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("迷你生態圈")  # 標題
    screen = pg.display.set_mode(window_size)
    bg_image = pg.image.load("images/background.png")  # 背景圖片
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 1000)

    # 隨機產生 25株紅蘿蔔
    for i in range(25):
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        carrot.CarrotSprite(x, y)  # 在 x, y 座標創建一個紅蘿蔔

    # 隨機產生 3隻兔子
    for i in range(10):
        x = random.randint(30, window_size[0] - 50)  # x座標
        y = random.randint(30, window_size[1] - 50)  # y座標
        RabbitSprite(x, y)  # 在 x, y 座標創建一隻兔子

    # 把所有物件集合起來
    sprites = pg.sprite.OrderedUpdates(carrot.group, group)

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
                sprites = pg.sprite.OrderedUpdates(carrot.group, group)
                # 若超過 550 隻兔子的話結束遊戲
                if len(group) > 550:
                    Done = True
                # 顯示有多少兔子在畫面上
                print(f"現在畫面上有 {len(group)} 隻兔子")
    pg.quit()  # 結束遊戲
