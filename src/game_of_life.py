import numpy as np


class GameOfLife(object):
    def __init__(self, size):
        self.__universe = np.zeros(size)

    @property
    def height(self):
        return self.__universe.shape[0]

    @property
    def width(self):
        return self.__universe.shape[1]

    def set_seed(self, seed, position):
        x_start, y_start = position[0], position[1]
        seed_array = np.array(seed)
        x_end, y_end = x_start + seed_array.shape[0], y_start + seed_array.shape[1]
        self.__universe[x_start:x_end, y_start:y_end] = seed_array

    def get_map(self):
        return self.__universe

    def __survival(self, x, y):
        """
        Compute one iteration of Life for one cell.
        :param x: x coordinate of cell in the universe
        :type x: int
        :param y: y coordinate of cell in the self.__universe
        :type y: int
        :param self.__universe: the self.__universe of cells
        :type self.__universe: np.ndarray
        """
        num_neighbours = (
            np.sum(self.__universe[x - 1 : x + 2, y - 1 : y + 2]) - self.__universe[x, y]
        )
        # The rules of Life
        if self.__universe[x, y]:
            if 2 <= num_neighbours <= 3:
                return 1
            else:
                return 0
        else:
            if num_neighbours == 3:
                return 1
            else:
                return 0

    def step(self):
        """
        Compute one iteration of Life for the self.__universe.
        :param self.__universe: initial self.__universe of cells
        :type self.__universe: np.ndarray
        :return: updated self.__universe of cells
        :rtype: np.ndarray
        """
        # Apply the survival function to every cell in the self.__universe
        next_step = [[self.__survival(i, j) for j in range(self.width)] for i in range(self.height)]
        self.__universe = np.array(next_step)
