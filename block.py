import pygame as pg

# 自己的 library
import env

# 設定起始參數
window_size = env.WINDOW_SIZE
border_size = 10


# 遊戲邊界
class BlockSprite(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


left_border = BlockSprite(-10, 0, border_size, window_size[1])  # 左邊界
right_border = BlockSprite(window_size[0], 0, border_size, window_size[1])  # 右邊界
bottom_border = BlockSprite(0, -border_size, window_size[0], border_size)  # 上邊界
top_border = BlockSprite(0, window_size[1], window_size[0], border_size)  # 下邊界

# 把邊界集合起來放到 group
group = pg.sprite.Group(left_border, right_border, bottom_border, top_border)
