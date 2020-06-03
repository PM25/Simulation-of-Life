import pygame as pg
import random

# 自己的 library
import env
import block
import grass
import turtle

# 設定起始變數
random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有狐狸物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
walk_images = []  # 讀取動畫圖片
for i in range(1, 10):
    fname = f"images/animation/FOX/fox{i}.png"
    walk_images.append(pg.transform.scale(pg.image.load(fname), (30, 30)))
eat_images = []  # 讀取動畫圖片
for i in range(1, 6):
    fname = f"images/animation/FOX/foxeat{i}.png"
    eat_images.append(pg.transform.scale(pg.image.load(fname), (30, 30)))


# 狐狸
class FoxSprite(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pass

    def update(self):
        pass

    def birth(self, direction):
        pass

    def chase(self):
        pos = pg.math.Vector2(self.x, self.y)
        if len(turtle.group) > 0:
            t = min(
                [t for t in turtle.group],
                key=lambda t: pos.distance_to(pg.math.Vector2(t.x, t.y)),
            )
            distance = pos.distance_to(pg.math.Vector2(t.x, t.y))
            if distance < 80:
                if t.x > self.x:
                    self.xStep = 2
                else:
                    self.xStep = -2

                if t.y > self.y:
                    self.yStep = 2
                else:
                    self.yStep = -2


# 程式從這裡開始
if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("迷你生態圈")  # 標題
    screen = pg.display.set_mode(window_size)
    bg_image = pg.image.load("images/background.png")
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 500)

    # 隨機產生 100株草
    for i in range(50):
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        grass.GrassSprite(x, y)  # 在 x, y 座標創建一株草

    # 隨機產生 5隻烏龜
    for i in range(10):
        x = random.randint(30, window_size[0] - 30)  # x座標
        y = random.randint(30, window_size[1] - 30)  # y座標
        turtle.TurtleSprite(x, y)  # 在 x, y 座標創建一隻烏龜

    # 隨機產生 5隻狐狸
    for i in range(3):
        x = random.randint(30, window_size[0] - 30)  # x座標
        y = random.randint(30, window_size[1] - 30)  # y座標
        FoxSprite(x, y)  # 在 x, y 座標創建一隻狐狸

    # 把所有物件集合起來
    sprites = pg.sprite.OrderedUpdates(grass.group, turtle.group, group)

    # 遊戲迴圈
    Done = False
    while not Done:
        clock.tick(FPS)  # 設定 FPS
        screen.blit(bg_image, [0, 0])  # 畫遊戲背景
        sprites.update()  # 執行所有 Sprite 物件裡面的 Update()
        sprites.draw(screen)  # 畫出所有 Sprite 物件到遊戲上
        pg.display.update()  # 更新畫面

        # 當有事件發生時 (例: 滑鼠、鍵盤)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Done = True  # 遊戲結束
            sprites = pg.sprite.OrderedUpdates(grass.group, turtle.group, group)
    pg.quit()  # 結束遊戲
