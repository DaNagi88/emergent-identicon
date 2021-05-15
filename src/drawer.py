import numpy as np
from src.constants import COLOR_BG


class Drawer:
    def __init__(self, imsize=[420, 420], color=[0, 0, 0], background=COLOR_BG):
        self.height = imsize[0]
        self.width = imsize[1]
        if isinstance(color, int):
            color = [color] * 3
        self.color = color
        if isinstance(background, int):
            background = [background] * 3
        self.background = background

    def draw(self, pattern):
        image = np.full([self.height, self.width, 3], COLOR_BG, dtype=np.float)
        grid_h = pattern.shape[0]
        grid_w = pattern.shape[1]

        block_h = self.height // (grid_h - 1)
        block_w = self.width // (grid_w - 1)
        margin_t = (self.height - (grid_h - 2) * block_h) // 2
        margin_l = (self.width - (grid_w - 2) * block_h) // 2
        slice_v = [0] + [margin_t + i * block_h for i in range(grid_h - 1)] + [self.height]
        slice_h = [0] + [margin_l + i * block_w for i in range(grid_w - 1)] + [self.width]

        for i in range(grid_h):
            for j in range(grid_w):
                if pattern[i, j]:
                    image[slice_v[i] : slice_v[i + 1], slice_h[j] : slice_h[j + 1]] = self.color
        return image
