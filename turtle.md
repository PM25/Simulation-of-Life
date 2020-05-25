\*需先完成 grass.py

# 烏龜 (物件 TurtleSprite)

    會隨機到處亂走，如果路上碰到了草則會停下來把它吃下去
    到達一定年紀以後會開始生小孩

-   ### 屬性(變數)

    -   x (x 座標)
    -   y (y 座標)
    -   energy = 0 (能量)
    -   xStep = random.randint(-3, 3) (每走一步 x 移動方向)
    -   yStep = random.randint(-3, 3) (每走一步 y 移動方向)
    -   圖片
        ```python
        self.image = 圖片( 程式碼 14 行 圖片大小為30x30 )
        ```
    -   rect 物件
        ```python
        self.rect = self.image.get_rect()
        ```
    -   物件位置
        ```python
        self.rect.center = [x座標, y座標]
        ```

-   ### 方法(Function)

    -   #### 初始化: \_\_init\_\_()
        -   設定屬性
        -   把自己加到 group(程式碼 11 行) 裡面去 `group.add(self)`
    -   #### 更新: update()

        -   隨機取得一個亂數 `random.random()`
        -   如果亂數 < 0.01 的話，隨機更改 xStep, yStep 的值
            ```python
            xStep = random.randint(-3, 3)
            yStep = random.randint(-3, 3)
            ```
        -   檢查有無跟牆壁碰撞
            ```python
            pg.sprite.spritecollideany(self, block.horiz_walls):
            pg.sprite.spritecollideany(self, block.vert_walls):
            ```
        -   如果跟水平牆壁碰撞的話
            ```python
            # 更改 y 移動的方向
            self.yStep = -self.yStep
            self.xStep = random.randint(-3, 3)
            ```
            如果跟垂直牆壁碰撞的話
            ```python
            # 更改 x 移動的方向
            self.xStep = -self.xStep
            self.yStep = random.randint(-3, 3)
            ```
        -   更新自身座標 ( self.x, self.y )
            ```python
            self.x += self.xStep / 3
            self.y += self.yStep / 3
            ```
        -   由自己的座標(self.x, self.y) 來更新圖片在遊戲中的位置 (self.rect.center)
            ```python
            self.rect.center = [x座標, y座標]
            ```

    -   吃草

        -   檢查有無跟草碰撞
            ```python
            if pg.sprite.spritecollide(單個物件(自己), 群體物件(grass.group), True):
            ```
        -   如果有碰撞的話
            ```python
            能量 += 10
            ```
        -   如果有碰撞的話，且能量大於 100 的話

            ```python
            self.birth(random.choice(["u", "d", "r", "l"]))
            ```

    -   #### 生小孩: birth()
        -   接受上、下、左、右四種方向
        -   在相對應的方向生出一隻烏龜
            `自己的 x座標: self.rect.center[0]`
            `自己的 y座標: self.rect.center[1]`
