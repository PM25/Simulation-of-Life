import pygame as pg
import random

# 自己的 library
import env
import block
import grass, carrot
import turtle, rabbit, fox

# 設定起始變數
random.seed(0)  # 設定亂數的種子
group = pg.sprite.Group()  # 變數 group用來存放所有兔子物件
window_size = env.WINDOW_SIZE  # 視窗大小
FPS = env.FPS  # 遊戲更新率
player_image = pg.transform.scale(pg.image.load("images/ninja.png"), (40, 40))
flip_player_image = pg.transform.flip(player_image, True, False)
star_image = pg.transform.scale(pg.image.load("images/star.png"), (15, 15))
rotate_star_images = []  # 讀取動畫圖片
for i in range(0, 20):
    rotate_star_images.append(pg.transform.rotate(star_image, 18 * i))

# 玩家
class PlayerSprite(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.xStep = 0
        self.yStep = 0
        self.face = "r"
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        group.add(self)

    def update(self):
        if self.face == "r":
            self.image = player_image
        elif self.face == "l":
            self.image = flip_player_image
        self.x += self.xStep
        self.y += self.yStep
        self.rect.center = [self.x, self.y]

    def move(self, direction):
        if direction == "u":
            self.yStep = -3
        if direction == "d":
            self.yStep = 3
        if direction == "r":
            self.xStep = 3
        if direction == "l":
            self.xStep = -3
        self.image = player_image
        self.face = direction

    def shoot(self):
        if self.face == "r":
            NinjaStarSprite(self.x, self.y, 10, 0)
        elif self.face == "l":
            NinjaStarSprite(self.x, self.y, -10, 0)
        elif self.face == "d":
            NinjaStarSprite(self.x, self.y, 0, 10)
        elif self.face == "u":
            NinjaStarSprite(self.x, self.y, 0, -10)

    def stop(self, direction):
        if direction == "x":
            self.xStep = 0
        if direction == "y":
            self.yStep = 0


# 飛鏢
class NinjaStarSprite(pg.sprite.Sprite):
    def __init__(self, x, y, xStep, yStep):  # x, y 為座標
        super().__init__()
        self.x = x
        self.y = y
        self.xStep = xStep
        self.yStep = yStep
        self.index = 0
        self.image = rotate_star_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        self.dead = False
        self.dead_index = 0
        group.add(self)

    def update(self):
        if self.dead:
            self.dead_index += 1
            if self.dead_index > 25:
                self.kill()
            return

        self.index += 1
        if self.index >= len(rotate_star_images):
            self.index = 0
        self.image = rotate_star_images[self.index]
        self.x += self.xStep
        self.y += self.yStep
        self.rect.center = [self.x, self.y]
        if self.index > window_size[0] or self.index > window_size[1]:
            self.get_kill()

        for c in (
            pg.sprite.spritecollide(self, turtle.group, False)
            + pg.sprite.spritecollide(self, rabbit.group, False)
            + pg.sprite.spritecollide(self, fox.group, False)
        ):
            c.get_kill()
            self.get_kill()
            break

    def get_kill(self):
        self.dead = True


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
        grass.group, carrot.group, turtle.group, rabbit.group, fox.group, group
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
                grass.group, carrot.group, turtle.group, rabbit.group, fox.group, group
            )
    pg.quit()  # 結束遊戲
