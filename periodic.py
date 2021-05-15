import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import argparse
import numpy as np

from src.game_of_life import GameOfLife
from src.identicon import parse_github_id
from src.drawer import Drawer


def main(
    size,
    username,
    distribute=[1, 1],
    quality=200,
    cmap="Purples",
    n_generations=50,
    interval=300,
    output=None,
):
    pattern, color = parse_github_id(username)
    game = GameOfLife(size, boundary="periodic")
    for i in range(-(distribute[0] // 2), (distribute[0] // 2) + 1):
        for j in range(-(distribute[1] // 2), (distribute[1] // 2) + 1):
            game.set_seed(
                pattern,
                [
                    (size[0] - pattern.shape[0]) // 2 + i * (pattern.shape[0] + 1),
                    (size[1] - pattern.shape[1]) // 2 + j * (pattern.shape[1] + 1),
                ],
            )
    drawer = Drawer(color=color)

    if not os.path.exists(output):
        os.makedirs(output)

    pattern_list = []
    print("running game of life")
    for i in tqdm(range(n_generations)):
        pattern = game.get_map()
        pattern_list.append(pattern)
        stable = game.step()
        if (not np.sum(pattern)) or stable:
            break

    print("generating images")
    for i, pattern in tqdm(enumerate(pattern_list), total=len(pattern_list)):
        plt.imsave(os.path.join(output, f"{i:08}.png"), drawer.draw(pattern))


def parse_args():
    parser = argparse.ArgumentParser(
        description="PyGameofLife. By default, produces 50 generations of the 'infinite' seed"
    )
    parser.add_argument(
        "-size",
        type=str,
        default="101,101",
        help="comma-separated dimensions of universe (y by x)",
    )
    parser.add_argument("-username", type=str, required=True)
    parser.add_argument("-n", type=int, default=50, help="number of universe iterations")
    parser.add_argument("-distribute", type=str, default="1,1")
    parser.add_argument("-quality", type=int, default=100, help="image quality in DPI")
    parser.add_argument("-cmap", type=str, default="Purples", help="colour scheme")
    parser.add_argument(
        "-interval",
        type=int,
        default=300,
        help="interval (in milliseconds) between iterations",
    )
    parser.add_argument("-output", type=str, default="output/frames", help="output path")

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    main(
        size=(
            int(args.size.split(",")[0]),
            int(args.size.split(",")[1]),
        ),
        username=args.username,
        distribute=(
            int(args.distribute.split(",")[0]),
            int(args.distribute.split(",")[1]),
        ),
        quality=args.quality,
        cmap=args.cmap,
        n_generations=args.n,
        interval=args.interval,
        output=args.output,
    )
