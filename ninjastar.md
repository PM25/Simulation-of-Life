# 玩家 (物件 PlayerSprite)

-   ### 方法(Function)

    -   #### 初始化: \_\_init\_\_(x, y, xStep)
        -   self.x = x 座標
        -   self.y = y 座標
        -   self.xStep = 0 (每走一步 x 移動方向)
        -   self.index = 0
        -   圖片
            ```python
            self.image = rotate_star_images[self.index]
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

        -   更新旋轉動畫

            ```python
            self.index += 1
            if self.index >= len(rotate_star_images):
                self.index = 0
            self.image = rotate_star_images[self.index]
            ```

        -   更新 self.x
            ```python
            self.x += self.xStep
            ```
        -   用 self.x, self.y 更新自身位置
            ```python
            self.rect.center = [自己的 x座標, 自己的 y座標]
            ```
        -   如果自己的座標(self.x, self.y) 超出遊戲邊界，把自己的殺掉`self.kill()`
            ```python
            遊戲的寬度: window_size[0]
            遊戲的高度: window_size[1]
            ```
        -   取出跟飛鏢碰撞的烏龜，並把烏龜跟飛鏢都殺掉
            ```python
            for t in pg.sprite.spritecollide(self, turtle.group, False):
                殺掉烏龜 t
                殺掉飛鏢 self
                break
            ```
