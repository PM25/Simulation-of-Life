import pygame as pg
import random

# 自己的 library
import env
import block
import grass, carrot
import turtle, rabbit

# 設定起始變數
random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有兔子物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
player_image = pg.transform.scale(pg.image.load("images/ninja.png"), (45, 45))
flip_player_image = pg.transform.flip(player_image, True, False)
star_image = pg.transform.scale(pg.image.load("images/star.png"), (15, 15))
rotate_star_images = []  # 讀取動畫圖片
for i in range(0, 20):
    rotate_star_images.append(pg.transform.rotate(star_image, 18 * i))

# 玩家
class PlayerSprite(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pass

    def update(self):
        pass

    def move(self, direction):
        pass

    def shoot(self):
        pass

    def stop(self, direction):
        pass


# 飛鏢
class NinjaStarSprite(pg.sprite.Sprite):
    def __init__(self, x, y, xStep):  # x, y 為座標
        super().__init__()
        pass

    def update(self):
        pass


player_sprite = PlayerSprite(window_size[0] // 2, window_size[1] // 2)


# 程式從這裡開始
if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("迷你生態圈")  # 標題
    screen = pg.display.set_mode(window_size)
    bg_image = pg.image.load("images/background.png")
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 1000)

    # 隨機產生 100株草
    for i in range(25):
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        grass.GrassSprite(x, y)  # 在 x, y 座標創建一株草
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        carrot.CarrotSprite(x, y)  # 在 x, y 座標創建一株草

    # 隨機產生 5隻烏龜
    for i in range(5):
        x = random.randint(30, window_size[0] - 30)  # x座標
        y = random.randint(30, window_size[1] - 30)  # y座標
        turtle.TurtleSprite(x, y)  # 在 x, y 座標創建一隻烏龜
        x = random.randint(30, window_size[0] - 30)  # x座標
        y = random.randint(30, window_size[1] - 30)  # y座標
        rabbit.RabbitSprite(x, y)  # 在 x, y 座標創建一隻烏龜

    # 把所有物件集合起來
    sprites = pg.sprite.OrderedUpdates(
        grass.group, carrot.group, turtle.group, rabbit.group, group
    )

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

            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                keys = pg.key.get_pressed()
                if keys[pg.K_UP]:
                    player_sprite.move("u")
                if keys[pg.K_DOWN]:
                    player_sprite.move("d")
                if keys[pg.K_LEFT]:
                    player_sprite.move("l")
                if keys[pg.K_RIGHT]:
                    player_sprite.move("r")
                if keys[pg.K_SPACE]:
                    player_sprite.shoot()

                if not (keys[pg.K_UP] or keys[pg.K_DOWN]):
                    player_sprite.stop("y")
                if not (keys[pg.K_LEFT] or keys[pg.K_RIGHT]):
                    player_sprite.stop("x")

            # 按下結束按鍵時
            if event.type == pg.QUIT:
                Done = True  # 遊戲結束
            # 更新物件內容
            sprites = pg.sprite.OrderedUpdates(
                grass.group, carrot.group, turtle.group, rabbit.group, group
            )
    pg.quit()  # 結束遊戲
