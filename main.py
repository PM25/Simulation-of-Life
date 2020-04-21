import random
import pygame as pg

# 自己的 library
import env
import grass
import turtle
import carrot
import rabbit

window_size = env.WINDOW_SIZE
FPS = env.FPS

# 程式開始
if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("迷你生態圈")  # 標題
    screen = pg.display.set_mode(window_size)
    bg_image = pg.image.load("images/background.png")
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 1000)

    # 隨機產生 100株草
    for i in range(100):
        x = random.randint(0, window_size[0]) // 25 * 25  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25  # y座標
        grass.GrassSprite(x, y)  # 在 x, y 座標創建一株草

    # 隨機產生 100個紅蘿蔔
    for i in range(100):
        x = random.randint(0, window_size[0]) // 25 * 25 - 5  # x座標
        y = random.randint(0, window_size[1]) // 25 * 25 - 5  # y座標
        carrot.CarrotSprite(x, y)  # 在 x, y 座標創建一株草

    # 隨機產生 5隻烏龜
    for i in range(3):
        x = random.randint(0, window_size[0])  # x座標
        y = random.randint(0, window_size[1])  # y座標
        turtle.TurtleSprite(x, y)  # 在 x, y 座標創建一隻烏龜

    # 隨機產生 5隻兔子
    for i in range(3):
        x = random.randint(0, window_size[0])  # x座標
        y = random.randint(0, window_size[1])  # y座標
        rabbit.RabbitSprite(x, y)  # 在 x, y 座標創建一隻兔子

    # 把所有物件集合起來
    sprites = pg.sprite.OrderedUpdates(
        grass.group, carrot.group, turtle.group, rabbit.group
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
            # 按下結束按鍵時
            if event.type == pg.QUIT:
                Done = True  # 遊戲結束
            if event.type == pg.USEREVENT:
                # 更新物件內容
                sprites = pg.sprite.OrderedUpdates(
                    grass.group, carrot.group, turtle.group, rabbit.group
                )
    pg.quit()  # 結束遊戲
