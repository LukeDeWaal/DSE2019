import numpy as np
import imageio as im
from typing import Union
from tqdm import tqdm
import threading


class SimGrid(object):

    def __init__(self, time: int, forest_size: Union[tuple, list, np.array]):

        self.time = int(time)
        self.forest_size = tuple(forest_size)
        # self.grid_size = tuple([s + 1 for s in self.forest_size])
        
        self.__r_evap = 0.05

        self.main_grid = np.zeros((self.time, *self.forest_size, 3), dtype=float)  # This grid will be used to convert to gif

        # These grids will be temporary grids used for calculations
        self.F_grid = np.random.rand(*self.forest_size)         # Fuel Grid
        self.I_grid = np.zeros(self.forest_size, dtype=float)  # Intensity Grid
        self.I_grid[self.forest_size[0] // 2, self.forest_size[1] // 2] = 1.0
        self.R_grid = np.zeros(self.forest_size, dtype=float)  # Retardant Grid

        self.__initialize_grid()

    def clear_space(self, topleft: tuple, size: tuple):
        """
        Make part of the grid unburnable
        :param topleft: top-left coordinate of the grid
        :param size: size of the grid
        """

        self.F_grid[topleft[0]:topleft[0]+size[0], topleft[1]: topleft[1]+size[1]] = np.zeros(size, dtype=float)

    def set_retardant(self, amount: float, topleft: tuple, size: tuple):
        """
        Set a certain part of the grid as retardant
        :param amount: Amount of retardant, 0-1
        :param topleft: top-left coordinate of the grid
        :param size: size of the grid
        """

        self.R_grid[topleft[0]:topleft[0]+size[0], topleft[1]: topleft[1]+size[1]] = np.ones(size)*amount

    @staticmethod
    def __number_check(number: float or np.ndarray):

        if type(number) == float:
            if 1 >= number >= 0:
                return number
            elif number < 0:
                return 0
            elif number > 1:
                return 1

        elif type(number) in [np.ndarray, np.array]:
            if 1 >= number.all() >= 0:
                return number
            elif number.any() < 0:
                number[number < 0] = 0
                return number
            elif number.any() > 1:
                number[number > 1] = 1
                return number

        else:
            raise TypeError("Wrong Input Type")

    def __initialize_grid(self):

        # Set up main grid
        self.main_grid[0, :, :, 0] = np.array(self.F_grid)
        self.main_grid[0, :, :, 1] = np.array(self.I_grid)
        self.main_grid[0, :, :, 2] = np.array(self.R_grid)

    def __kernel_average(self, position: tuple):

        size = [3, 3]
        xrange = [position[0] - 1, position[0] + 1]
        yrange = [position[1] - 1, position[1] + 1]

        if xrange[0] < 0:
            xrange[0] = 0
            size[0] = 2

        elif xrange[1] > self.forest_size[0]:
            xrange[1] = self.forest_size[0]
            size[0] = 2

        if yrange[0] < 0:
            yrange[0] = 0
            size[1] = 2

        elif yrange[1] > self.forest_size[0]:
            yrange[1] = self.forest_size[0]
            size[1] = 2

        return np.average(self.I_grid[xrange[0]:xrange[1]+1, yrange[0]:yrange[1]+1])

    def __intensity_averages(self):

        avgs = np.zeros(self.forest_size)
        for x in range(self.forest_size[0]):
            for y in range(self.forest_size[1]):
                avgs[x, y] = self.__kernel_average((x, y))

        return avgs

    def __update_fuel(self, t: int):

        old_grid = np.array(self.F_grid)
        self.F_grid = self.__number_check(self.F_grid * (1 / (1 + self.I_grid)))
        self.F_grid[self.F_grid < 0.0001] = 0
        self.main_grid[t, :, :, 0] = self.F_grid
        return old_grid - self.F_grid

    def __update_intensities(self, t: int, delta_fuel: np.array):

        old_grid = np.array(self.I_grid)
        iavgs = self.__intensity_averages()
        self.I_grid = self.__number_check((self.I_grid*(1 - np.sqrt(self.R_grid))/(1 - delta_fuel) + iavgs)*self.F_grid)
        self.I_grid[self.I_grid < 0.0001] = 0
        self.main_grid[t, :, :, 1] = self.I_grid
        return old_grid - self.I_grid

    def __update_retardant(self, t: int, delta_intensity: np.array):

        old_grid = np.array(self.R_grid)
        self.R_grid = self.__number_check((1 - self.__r_evap)*self.R_grid)
        self.main_grid[t, :, :, 2] = self.R_grid
        return old_grid - self.R_grid

    def __update(self, t: int):

        delta_fuel = self.__update_fuel(t)
        delta_intensity = self.__update_intensities(t, delta_fuel)
        delta_retardant = self.__update_retardant(t, delta_intensity)

    def run(self):

        for t in tqdm(range(self.time)):
            self.__update(t)



if __name__ == '__main__':

    S = SimGrid(100, (300, 300))
    S.run()
    a = S.main_grid