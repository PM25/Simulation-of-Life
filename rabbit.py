import pygame as pg
import random

# 自己的 library
import env
import carrot

# 設定起始變數
random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有兔子物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
image = pg.transform.scale(pg.image.load("images/rabbit.png"), (30, 30))  # 讀取兔子圖片


# TODO: 幫我完成下面這個物件!
# 兔子
class RabbitSprite(pg.sprite.Sprite):
    def __init__(self, x, y):  # x, y 為座標
        super().__init__()
        self.day = 0
        self.age = 0
        self.direct = None #?
        self.step = 0
        self.energy = 10 
        self.success = False #?
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.check()


    def update(self):
        self.day += 1
        if self.day == 50:
            self.age += 1
            self.energy -= 2
            self.day = random.randint(0,50)
            if 15 <= self.age <= 20:
                self.birth(random.choice(['u','d','r','l']))
                #能量-12?
            if self.age > 30:
                self.kill()

    def walk(self):
        if self.step = 0:
            

    def birth(self, direction):
         if direction == 'u':
             self.y -=25
         if direction == 'd':
             self.y +=25
         if direction == 'r':
             self.x +=25
         if direction == 'l':
             self.x -=25

    def check(self):
        pass


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
    for i in range(3):
        x = random.randint(0, window_size[0])  # x座標
        y = random.randint(0, window_size[1])  # y座標
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
