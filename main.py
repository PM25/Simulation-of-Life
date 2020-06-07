import random
import pygame as pg
from time import sleep

# 自己的 library
import env, block
import grass, carrot
import turtle, rabbit, fox, player

window_size = env.WINDOW_SIZE
FPS = env.FPS

# 程式開始
if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("迷你生態圈")  # 標題
    screen = pg.display.set_mode(window_size)
    bg_image = pg.transform.scale(
        pg.image.load("images/background.png"), (window_size[0], window_size[1])
    )
    font = pg.font.SysFont("microsoftyaheimicrosoftyaheiui", 30)
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 1000)

    # 隨機產生 100株草
    for i in range(50):
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        grass.GrassSprite(x, y)  # 在 x, y 座標創建一株草
        x = random.randint(0, window_size[0]) // 25 * 25 - 5  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25 - 5  # y座標
        carrot.CarrotSprite(x, y)  # 在 x, y 座標創建一株草

    # 隨機產生 5隻烏龜
    for i in range(10):
        x = random.randint(0, window_size[0])  # x座標
        y = random.randint(0, window_size[1])  # y座標
        turtle.TurtleSprite(x, y)  # 在 x, y 座標創建一隻烏龜
        x = random.randint(0, window_size[0])  # x座標
        y = random.randint(0, window_size[1])  # y座標
        rabbit.RabbitSprite(x, y)  # 在 x, y 座標創建一隻兔子

    for i in range(3):
        x = random.randint(0, window_size[0])
        y = random.randint(0, window_size[1])
        fox.FoxSprite(x, y)

    # 把所有物件集合起來
    sprites = pg.sprite.OrderedUpdates(
        grass.group, carrot.group, turtle.group, rabbit.group, fox.group, player.group
    )

    # 遊戲迴圈
    Done = False
    Pause = True
    Win = False
    while not Done:
        clock.tick(FPS)  # 設定 FPS
        screen.blit(bg_image, [0, 0])  # 畫遊戲背景
        sprites.update()  # 執行所有 Sprite 物件裡面的 Update()
        sprites.draw(screen)  # 畫出所有 Sprite 物件到遊戲上
        pg.display.update()  # 更新畫面

        while Pause:
            text = font.render("Hello World", True, (255, 255, 255))
            screen.blit(text, (100, 100))
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    Pause = False
                if event.type == pg.QUIT:
                    Done = True
                    Pause = False

        # 當有事件發生時 (例: 滑鼠、鍵盤)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                keys = pg.key.get_pressed()
                if keys[pg.K_UP]:
                    player.player_sprite.move("u")
                if keys[pg.K_DOWN]:
                    player.player_sprite.move("d")
                if keys[pg.K_LEFT]:
                    player.player_sprite.move("l")
                if keys[pg.K_RIGHT]:
                    player.player_sprite.move("r")
                if keys[pg.K_SPACE]:
                    player.player_sprite.shoot()

                if not (keys[pg.K_UP] or keys[pg.K_DOWN]):
                    player.player_sprite.stop("y")
                if not (keys[pg.K_LEFT] or keys[pg.K_RIGHT]):
                    player.player_sprite.stop("x")

            # 按下結束按鍵時
            if event.type == pg.QUIT:
                Done = True  # 遊戲結束
            if event.type == pg.USEREVENT:
                x = random.randint(0, window_size[0]) // 25 * 25  # x座標
                y = random.randint(0, window_size[1]) // 25 * 25  # y座標
                grass.GrassSprite(x, y)  # 在 x, y 座標創建一株草
                x = random.randint(0, window_size[0]) // 25 * 25 - 5  # x座標
                y = random.randint(0, window_size[1]) // 25 * 25 - 5  # y座標
                carrot.CarrotSprite(x, y)  # 在 x, y 座標創建一株草
            if len(fox.group) == 0:
                Pause = True
                Win = True
            # 更新物件內容
            sprites = pg.sprite.OrderedUpdates(
                grass.group,
                carrot.group,
                turtle.group,
                rabbit.group,
                fox.group,
                player.group,
            )
    pg.quit()  # 結束遊戲
