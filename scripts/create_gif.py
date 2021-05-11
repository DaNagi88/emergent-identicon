from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

from src.constants import SEEDS
from src.game_of_life import GameOfLife


def main(
    universe_size,
    seed,
    seed_position,
    quality=200,
    cmap="Purples",
    n_generations=50,
    interval=300,
    output=None,
):
    """
    Animate the Game of Life.
    :param universe_size: dimensions of the universe
    :type universe_size: tuple (int, int)
    :param seed: initial starting array
    :type seed: list of lists, np.ndarray
    :param seed_position: coordinates where the top-left corner of the seed array should
                          be pinned
    :type seed_position: tuple (int, int)
    :param cmap: the matplotlib cmap that should be used
    :type cmap: str
    :param n_generations: number of universe iterations, defaults to 30
    :param n_generations: int, optional
    :param interval: time interval between updates (milliseconds), defaults to 300ms
    :param interval: int, optional
    :param save: whether the animation should be saved, defaults to False
    :param save: bool, optional
    """

    # Animate
    game = GameOfLife(universe_size)
    game.set_seed(seed, seed_position)
    fig = plt.figure(dpi=quality)
    plt.axis("off")
    ims = []
    for i in tqdm(range(n_generations)):
        ims.append((plt.imshow(game.get_image(), cmap=cmap),))
        game.step()
    im_ani = animation.ArtistAnimation(fig, ims, interval=interval, repeat_delay=3000, blit=True)
    # Optional: save the animation, with a name based on the seed.
    if output is not None:
        im_ani.save(output, writer="imagemagick")


def parse_args():
    parser = argparse.ArgumentParser(
        description="PyGameofLife. By default, produces 50 generations of the 'infinite' seed"
    )
    parser.add_argument(
        "--universe-size",
        type=str,
        default="100,100",
        help="comma-separated dimensions of universe (x by y)",
    )
    parser.add_argument(
        "-seed", type=str, default="infinite", help="seed for Life, see readme for list"
    )
    parser.add_argument("-n", type=int, default=50, help="number of universe iterations")
    parser.add_argument("-quality", type=int, default=100, help="image quality in DPI")
    parser.add_argument("-cmap", type=str, default="Purples", help="colour scheme")
    parser.add_argument(
        "-interval",
        type=int,
        default=300,
        help="interval (in milliseconds) between iterations",
    )
    parser.add_argument(
        "--seed-position",
        type=str,
        default="40,40",
        help="comma-separated coordinates of seed",
    )
    parser.add_argument("-output", type=str, default="output.gif", help="output path")

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    main(
        universe_size=(
            int(args.universe_size.split(",")[0]),
            int(args.universe_size.split(",")[1]),
        ),
        seed=SEEDS[args.seed],
        quality=args.quality,
        cmap=args.cmap,
        seed_position=(
            int(args.seed_position.split(",")[0]),
            int(args.seed_position.split(",")[1]),
        ),
        n_generations=args.n,
        interval=args.interval,
        output=args.output,
    )
