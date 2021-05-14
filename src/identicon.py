import hashlib
import colorsys
import numpy as np
from constants import COLOR_BG, ID_WIDTH, ID_HEIGHT, N_BLOCK


def get_hash(userid):
    if isinstance(userid, int):
        userid = str(userid).encode()
    if isinstance(userid, str):
        userid = userid.encode()
    return hashlib.md5(userid).hexdigest()


def get_pattern(md5):
    return [int(i, 16) % 2 == 0 for i in md5[:15]]


def get_color(md5):
    hue = int(md5[25:28], 16) / 4095
    saturation = (65 - int(md5[28:30], 16) * 20 / 255) / 100
    lightness = (75 - int(md5[30:32], 16) * 20 / 255) / 100
    return colorsys.hls_to_rgb(hue, lightness, saturation)


def create_identicon(userid):
    md5 = get_hash(userid)
    pattern = get_pattern(md5)
    color = get_color(md5)

    image = np.full([ID_HEIGHT, ID_WIDTH, 3], COLOR_BG, dtype=np.float)

    block_width = ID_WIDTH // (N_BLOCK + 1)
    block_height = ID_HEIGHT // (N_BLOCK + 1)
    margin_l = (ID_WIDTH - N_BLOCK * block_width) // 2
    margin_t = (ID_HEIGHT - N_BLOCK * block_height) // 2

    for j in range((N_BLOCK + 1) // 2):
        for i in range(N_BLOCK):
            if pattern[i + j * 5]:
                image[
                    margin_t + i * block_height : margin_t + (i + 1) * block_height,
                    margin_l + (j + 2) * block_width : margin_l + (j + 3) * block_width,
                ] = np.array(color)

    image[:, : ID_WIDTH // 2] = image[:, : ID_WIDTH // 2 - 1 : -1]
    return image
