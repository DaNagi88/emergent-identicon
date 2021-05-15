import numpy as np


class GameOfLife(object):
    def __init__(self, size, boundary=None):
        self.__field = np.zeros(size)
        if boundary == "periodic":
            self.get_neighbor = self.get_neighbor_periodic
        else:
            self.get_neighbor = self.get_neighbor_dirichlet

    @property
    def height(self):
        return self.__field.shape[0]

    @property
    def width(self):
        return self.__field.shape[1]

    def get_neighbor_dirichlet(self, i, j):
        neighbors = [
            self.__field[y, x]
            for y in range(i - 1, i + 2)
            for x in range(j - 1, j + 2)
            if 0 <= x < self.width and 0 <= y < self.height
        ]
        return neighbors

    def get_neighbor_periodic(self, i, j):
        neighbors = [
            self.__field[y % self.height, x % self.width]
            for y in range(i - 1, i + 2)
            for x in range(j - 1, j + 2)
        ]
        return neighbors

    def set_seed(self, seed, position):
        x_start, y_start = position[0], position[1]
        seed_array = np.array(seed)
        x_end, y_end = x_start + seed_array.shape[0], y_start + seed_array.shape[1]
        self.__field[x_start:x_end, y_start:y_end] = seed_array

    def get_map(self):
        return self.__field

    def __update(self, i, j):
        neighbors = self.get_neighbor(i, j)
        num = sum(neighbors) - self.__field[i, j]
        # num = np.sum(self.__field[i - 1 : i + 2, j - 1 : j + 2]) - self.__field[i, j]
        if self.__field[i, j]:
            if 2 <= num <= 3:
                return 1
            else:
                return 0
        else:
            if num == 3:
                return 1
            else:
                return 0

    def step(self):
        next_step = np.array(
            [[self.__update(i, j) for j in range(self.width)] for i in range(self.height)]
        )
        stable = np.all(self.__field == next_step)
        self.__field = np.array(next_step)

        return stable
