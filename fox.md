# 狐狸 (物件 FoxSprite)

    會隨機到處亂走，如果路上碰到了烏龜或兔子則會把它吃下去
    能量超過一定的值以後會生小孩

-   ### 方法(Function)

    -   #### 初始化: \_\_init\_\_(x, y)
        -   x (x 座標)
        -   y (y 座標)
        -   energy = 0 (能量)
        -   xStep = random.randint(-2, 2) (每走一步 x 移動方向)
        -   yStep = random.randint(-2, 2) (每走一步 y 移動方向)
        -   index = 0
        -   圖片
            ```python
            self.image = self.images[self.index]
            ```
        -   rect 物件
            ```python
            self.rect = self.image.get_rect()
            ```
        -   物件位置
            ```python
            self.rect.center = [x座標, y座標]
            ```
        -   把自己加到 group(程式碼 11 行) 裡面去
            ```python
            group.add(self)
            ```
    -   #### 更新: update()

        -   走路動畫
            ```python
            self.index += 1
            if self.index >= len(walk_images):
                self.index = 0
            self.image = walk_images[self.index]
            ```
        -   隨機取得一個亂數 `random.random()`
        -   如果亂數 < 0.01 的話，隨機更改 xStep, yStep 的值 (-2 ~ 2)
            ```python
            xStep = random.randint(-2, 2)
            yStep = random.randint(-2, 2)
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
            self.xStep = random.randint(-2, 2)
            ```
            如果跟垂直牆壁碰撞的話
            ```python
            # 更改 x 移動的方向
            self.xStep = -self.xStep
            self.yStep = random.randint(-2, 2)
            ```
        -   更新自身座標 ( self.x, self.y )
            ```python
            self.x += self.xStep
            self.y += self.yStep
            ```
        -   檢查有無超出邊界
            ```python
            if self.x <= 30:
                self.x = 30
            if self.y <= 30:
                self.y = 30
            if self.x >= window_size[0] - 30:
                self.x = window_size[0] - 30
            if self.y >= window_size[1] - 30:
                self.y = window_size[1] - 30
            ```
        -   由自己的座標(self.x, self.y) 來更新圖片在遊戲中的位置 (self.rect.center)

            ```python
            self.rect.center = [x座標, y座標]
            ```

        -   吃烏龜

            -   檢查有無跟烏龜碰撞
                ```python
                pg.sprite.spritecollide(單個物件(自己), 群體物件(carrot.group), True)
                ```
            -   如果有碰撞的話
                ```python
                能量 += 10
                ```
            -   如果有碰撞的話，且能量大於 30 的話

                ```python
                self.birth(...)
                能量 = 0
                ```

    -   #### 追蹤獵物: chase()

        -   取得自身座標
            ```python
            pos = pg.math.Vector2(self.x, self.y)
            ```
        -   如果烏龜的數量大於 0 的話
            ```python
            len(turtle.group)
            ```
        -   找出離狐狸最近的烏龜
            ```python
            t = min(
                [t for t in turtle.group],
                key=lambda t: pos.distance_to(pg.math.Vector2(t.x, t.y)),
            )
            ```
        -   計算烏龜跟狐狸間的距離
            ```python
            distance = pos.distance_to(pg.math.Vector2(t.x, t.y))
            ```
        -   如果距離小於 80 的話，更新走路方向

            ```python
            if t.x > self.x:
                self.xStep = 2
            else:
                self.xStep = -2

            if t.y > self.y:
                self.yStep = 2
            else:
                self.yStep = -2
            ```

    -   #### 生小孩: birth(direction)
        -   如果 direction 等於 "u" (up)
            ```python
            FoxSprite(自己的 x座標, 自己的 y座標 - 30)
            ```
        -   如果 direction 等於 "d" (down)
            ```python
            FoxSprite(...)
            ```
        -   如果 direction 等於 "l" (left)
            ```python
            FoxSprite(...)
            ```
        -   如果 direction 等於 "r" (right)
            ```python
            FoxSprite(...)
            ```
        -   在相對應的方向生出狐狸
            `自己的 x座標: self.rect.x`
            `自己的 y座標: self.rect.y`
