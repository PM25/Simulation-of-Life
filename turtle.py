import pygame as pg
import random

# 自己的 library
import env
import block
import grass

# 設定起始變數
random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有烏龜物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
image = pg.transform.scale(pg.image.load("images/turtle.png"), (30, 30))  # 讀取烏龜圖片


# TODO: 幫我完成下面這個物件!
# 烏龜
class TurtleSprite(pg.sprite.Sprite):
    def __init__(self, x, y):  # x, y 為座標
        super().__init__()
        self.image=image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.engery=0
        self.x=x
        self.y=y
        self.xStep=random.randint(-3,3)
        self.yStep=random.randint(-3,3)
        group.add(self)
        

    def update(self):
        r=random.random()
        if r<0.01:
            self.xStep = random.randint(-3, 3)
            self.yStep = random.randint(-3, 3)
        # if pg.sprite.spritecollideany(self, block.horiz_walls):
        #     self.yStep = -self.yStep
        #     self.xStep = random.randint(-3, 3)
        # if pg.sprite.spritecollideany(self, block.vert_walls):
        #     self.xStep = -self.xStep
        #     self.yStep = random.randint(-3, 3)
        self.x += self.xStep / 3
        self.y += self.yStep / 3
        self.rect.center = [self.x, self.y]

        if pg.sprite.spritecollide(self, grass.group, True):
            self.engery+=10
            if self.engery>100:
                self.birth()



    


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
    for i in range(3):
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
