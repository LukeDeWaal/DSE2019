import numpy as np
import imageio as im
from typing import Union
from tqdm import tqdm


class SimGrid(object):

    def __init__(self, time: int, forest_size: Union[tuple, list, np.array]):

        self.time = int(time)
        self.size = tuple(forest_size)

        self.main_grid = np.zeros((self.time, *self.size, 3), dtype=float)
        self.F_grid = np.random.rand(*self.size)
        self.I_grid = np.zeros(self.size, dtype=float)
        self.R_grid = np.zeros(self.size, dtype=float)

    def clear_space(self, topleft: tuple, size: tuple):

        self.F_grid[topleft[0]:topleft[0]+size[0], topleft[1]: topleft[1]+size[1]] = np.zeros(size, dtype=float)

    def set_retardant(self, amount: float, topleft: tuple, size: tuple):

        self.R_grid[topleft[0]:topleft[0]+size[0], topleft[1]: topleft[1]+size[1]] = np.ones(size)*amount

    def __initialize_grid(self):

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.main_grid[0, x, y, 0] = np.array(self.F_grid)
                self.main_grid[0, x, y, 1] = np.array(self.I_grid)
                self.main_grid[0, x, y, 2] = np.array(self.R_grid)

    def __update_fuel(self, t: int):

        old_grid = np.array(self.F_grid)
        self.F_grid = self.F_grid * (1 / (1 + self.I_grid))
        self.main_grid[t, :, :, 0] = self.F_grid

    def __update_intensities(self, t: int, delta_fuel: np.array):

        self.I_grid = self.I_grid/(1 - delta_fuel)