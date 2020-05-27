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


# TODO: 幫我完成下面這個物件!
# 草
class GrassSprite(pg.sprite.Sprite):
    def __init__(self, x, y):  # x, y 為座標
        super().__init__()
        self.image=image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.day=0
        self.age=0
        self.a=x
        self.b=y
        self.check()


        

    def check(self):
        co = pg.sprite.spritecollideany(self,group)
        co1 =pg.sprite.spritecollideany(self,block.group)
        if co == None:
            group.add(self)
    
    def birth(self, direction):
        if direction=="u":
            self.b-=25
        if direction=="d":
            self.b+=25
        if direction=="r":
            self.a-=25
        if direction=="l":
            self.a+=25 
            grass=GrassSprite(self.a,self.b)
          
        

    
    def update(self):
        self.day+=1 
        if self.day==50:
            self.age+=1
            self.day=random.randint(0,50)
            if 2 <= self.age <=13:
                self.birth(random.choice(["u","d","l","r"]))
            if 15 < self.age:
                self.kill()
            



# 程式開始
if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("迷你生態圈")  # 標題
    screen = pg.display.set_mode(window_size)
    bg_image = pg.image.load("images/background.png")  # 背景圖片
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 1000)

    # 隨機產生 5株草
    for i in range(5):
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        GrassSprite(x, y)  # 在 x, y 座標創建一株草

    # 遊戲迴圈
    Done = False
    while not Done:
        clock.tick(FPS)  # 設定 FPS
        screen.blit(bg_image, [0, 0])  # 畫遊戲背景
        group.update()  # 執行所有 GrassSprite 裡面的 Update()
        group.draw(screen)  # 畫出所有 GrassSprite 到遊戲上
        pg.display.update()  # 更新畫面

        # 當有事件發生時 (例: 滑鼠、鍵盤)
        for event in pg.event.get():
            # 按下結束按鍵時
            if event.type == pg.QUIT:
                Done = True  # 遊戲結束
            if event.type == pg.USEREVENT:
                # 若超過 550 株草的話結束遊戲
                if len(group) > 550:
                    Done = True
                # 顯示有多少草在畫面上
                print(f"現在畫面上有 {len(group)} 株草")
    pg.quit()  # 結束遊戲
