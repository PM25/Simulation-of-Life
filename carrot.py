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


# TODO: 幫我完成下面這個物件!
# 紅蘿蔔
class CarrotSprite(pg.sprite.Sprite):
    def __init__(self, x, y):  # x, y 為座標
        super().__init__()
        self.x = x
        self.y = y
        self.day = 0
        self.age = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.check()
        

    def update(self):
        self.day += 1
        if self.day == 50:
            self.age += 1
            self.day = random.randint(0,50)
            if 3 <= self.age <=15:
                self.birth(random.choice(['u','d','r','l']))
            if self.age > 20:
                self.kill()
                
                
    def birth(self, direction):
         if direction == 'u':
             self.y -=25
         if direction == 'd':
             self.y +=25
         if direction == 'r':
             self.x +=25
         if direction == 'l':
             self.x -=25
         carrot = CarrotSprite(self.x , self.y)
            

    def check(self):
        co = pg.sprite.spritecollideany(self,group)
        if co == None:
            group.add(self)

# 程式開始
if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("迷你生態圈")  # 標題
    screen = pg.display.set_mode(window_size)
    bg_image = pg.image.load("images/background.png")  # 背景圖片
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 1000)

    # 隨機產生 5株紅蘿蔔
    for i in range(5):
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        CarrotSprite(x, y)  # 在 x, y 座標創建一株紅蘿蔔

    # 遊戲迴圈
    Done = False
    while not Done:
        clock.tick(FPS)  # 設定 FPS
        screen.blit(bg_image, [0, 0])  # 畫遊戲背景
        group.update()  # 執行所有 CarrotSprite 裡面的 Update()
        group.draw(screen)  # 畫出所有 CarrotSprite 到遊戲上
        pg.display.update()  # 更新畫面

        # 當有事件發生時 (例: 滑鼠、鍵盤)
        for event in pg.event.get():
            # 按下結束按鍵時
            if event.type == pg.QUIT:
                Done = True  # 遊戲結束
            if event.type == pg.USEREVENT:
                # 若超過 550 株紅蘿蔔的話結束遊戲
                if len(group) > 550:
                    Done = True
                # 顯示有多少紅蘿蔔在畫面上
                print(f"現在畫面上有 {len(group)} 個紅蘿蔔")
    pg.quit()  # 結束遊戲
