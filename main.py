import random
import pygame as pg
from time import sleep
from pathlib import Path
import datetime

# 自己的 library
import env, block
import grass, carrot
import turtle, rabbit, fox, player

window_size = env.WINDOW_SIZE
FPS = env.FPS

# 程式開始
if __name__ == "__main__":
    pg.init()
    pg.font.init()
    pg.display.set_caption("迷你生態圈")  # 標題
    screen = pg.display.set_mode(window_size)
    bg_image = pg.transform.scale(
        pg.image.load("images/background.png"), (window_size[0], window_size[1])
    )
    font = pg.font.Font(str(Path("fonts/jf-openhuninn-1.1.ttf")), 45)
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 500)
    first_time = datetime.datetime.now()

    def show_text(text, x, y):
        text = font.render(text, True, (60, 60, 60))
        text_rect = text.get_rect()
        text_rect.center = [x, y]
        screen.blit(text, text_rect)

    def show_multiline(texts, x, y):
        line = len(texts)
        pg.draw.rect(
            screen,
            (245, 245, 245),
            (
                window_size[0] // 10,
                window_size[1] // 10,
                window_size[0] // 10 * 8,
                window_size[1] // 10 * 8,
            ),
        )
        for i, text in enumerate(texts):
            show_text(text, x, y - (line // 2 - i) * 45)

    for i in range(100):
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        grass.GrassSprite(x, y)  # 在 x, y 座標創建一株草
        x = random.randint(0, window_size[0]) // 25 * 25 - 5  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25 - 5  # y座標
        carrot.CarrotSprite(x, y)  # 在 x, y 座標創建一株胡蘿蔔

    for i in range(10):
        x = random.randint(0, window_size[0])  # x座標
        y = random.randint(0, window_size[1])  # y座標
        turtle.TurtleSprite(x, y)  # 在 x, y 座標創建一隻烏龜
    for i in range(5):
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
            if not Win:
                show_multiline(
                    [
                        "遊戲說明",
                        "-------------",
                        "鍵盤上下左右控制玩家移動",
                        "空白鍵發射飛鏢",
                        "打死畫面上的所有狐狸即可獲得勝利",
                        "案任意鍵開始遊戲!",
                    ],
                    window_size[0] // 2,
                    window_size[1] // 2,
                )
            else:
                difference = end_time - first_time
                seconds_in_day = 24 * 60 * 60
                minutes, seconds = divmod(
                    difference.days * seconds_in_day + difference.seconds, 60
                )
                show_multiline(
                    [
                        "恭喜獲勝!",
                        "----------",
                        f"遊戲時間: {minutes}分, {seconds}秒",
                        f"死亡數: 烏龜x{turtle.dead_count}, 兔子x{rabbit.dead_count}, 狐狸x{fox.dead_count}",
                        "----------",
                        "美工設計: 王姵淇",
                        "程式開發: 黃品硯, 李德珊, 許家菱, 王姵淇",
                    ],
                    window_size[0] // 2,
                    window_size[1] // 2,
                )
                # show_text("恭喜獲勝!!", window_size[0] // 2, window_size[1] // 2)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_ESCAPE]:
                        Done = True
                    if not Win:
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
                if keys[pg.K_p]:
                    Pause = True
                if keys[pg.K_ESCAPE]:
                    Done = True

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
                end_time = datetime.datetime.now()
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
