import json
import hashlib
import colorsys
from urllib.request import urlopen
import numpy as np


def get_github_id(login_name):
    url = f"https://api.github.com/users/{login_name}"
    with urlopen(url) as webfile:
        string = webfile.read().decode()
    user_info = json.loads(string)
    user_id = user_info.get("id")

    return user_id


def get_hash(userid):
    if isinstance(userid, int):
        userid = str(userid).encode()
    if isinstance(userid, str):
        userid = userid.encode()
    return hashlib.md5(userid).hexdigest()


def get_pattern(md5):
    code = [int(i, 16) % 2 == 0 for i in md5[:15]]
    pattern = np.zeros((5, 5), dtype=np.int)
    for digit, sign in enumerate(code):
        row = digit % 5
        column = digit // 5 + 2
        pattern[row, column] = sign
    pattern[:, :2] = pattern[:, :2:-1]
    return pattern


def get_color(md5):
    hue = int(md5[25:28], 16) / 4095
    saturation = (65 - int(md5[28:30], 16) * 20 / 255) / 100
    lightness = (75 - int(md5[30:32], 16) * 20 / 255) / 100
    return colorsys.hls_to_rgb(hue, lightness, saturation)


def parse_github_id(username):
    userid = get_github_id(username)
    md5 = get_hash(userid)
    pattern = get_pattern(md5)
    color = get_color(md5)

    return pattern, color
