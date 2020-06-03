# 玩家 (物件 PlayerSprite)

-   ### 方法(Function)

    -   #### 初始化: \_\_init\_\_(x, y)
        -   self.x = x 座標
        -   self.y = y 座標
        -   self.xStep = 0 (每走一步 x 移動方向)
        -   self.yStep = 0 (每走一步 y 移動方向)
        -   self.face = 'l' (玩家面對的方向 LEFT or RIGHT)
        -   圖片
            ```python
            self.image = player_image
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

        -   更新 self.x, self.y
            ```python
            self.x += self.xStep
            self.y += self.yStep
            ```
        -   用 self.x, self.y 更新自身位置
            ```python
            self.rect.center = [自己的 x座標, 自己的 y座標]
            ```

    -   #### 移動: move(direction)

        -   如果 direction 等於 "u" (up)
            ```python
            self.yStep = -3
            ```
        -   如果 direction 等於 "d" (down)
            ```python
            ... (自己類推)
            ```
        -   如果 direction 等於 "l" (left)

            ```python
            ... (自己類推)

            #更新面對的方向
            self.image = flip_player_image
            self.face = direction
            ```

        -   如果 direction 等於 "r" (right)

            ```python
            ... (自己類推)

            #更新面對的方向
            self.image = player_image
            self.face = direction
            ```

    -   #### 射擊: shoot()
        -   如果玩家面對右邊的話
            ```python
            NinjaStarSprite(起始 x座標, 起始 y座標, 10)
            ```
        -   如果玩家面對左的話
            ```python
            NinjaStarSprite(起始 x座標, 起始 y座標, -10)
            ```
    -   #### 停止移動: stop(direction)
        -   如果 direction 等於 "x"
            ```python
            把 self.xStep 設為 0
            ```
        -   如果 direction 等於 "y"
            ```python
            把 self.yStep 設為 0
            ```
