import numpy as np
import imageio as im
from typing import Union

class Grid(object):

    def __init__(self, time: int, forest_size: Union[tuple, list, np.array], p: float = 0.6):
        """
        Initialize the grid object to execute a simulation
        :param time:
        :param forest_size:
        :param p:
        """

        self.time = time

        if type(forest_size) in (tuple, list, np.array):
            self.size = tuple(forest_size)

        self.grid = np.zeros((time, *self.size), dtype=int)
        self.coloured_grid = np.zeros((time, *self.size, 3), dtype=int)
        self.probability = p

        self.__initialize_grid(clearspot_1=((8, 100), (100, 75)))

    def run(self, name: str, path: str):
        """
        Run simulation
        :param name: name of file
        :param path: path to older in which to store
        :return:
        """

        self.__simulate()
        self.__colour_graphics()
        self.__crop()
        self.__save_simulation(name, path)

    def clear_spot(self, t: int, shape: Union[tuple, list, np.array], position: Union[tuple, list, np.array]):
        """
        Clears spot at designated area and time
        :param t: time at which to clear the spot
        :param shape: shape of cleared (square) spot
        :param position: position of burned mark
        """
        self.grid[t, position[0]:position[0] + shape[0], position[1]:position[1] + shape[1]] = np.zeros(shape=shape)

    def __initialize_grid(self, **kwargs):
        """
        Sets up first grid
        """

        # creates random fuel and clear cells to initialise cell states.
        self.grid[0,:,:] = np.random.choice([0,1],size=self.size,p=[1-self.probability,self.probability])

        # set the middle cell on fire
        self.grid[0, self.size[0] // 2, self.size[1] // 2] = 2

        for key, value in kwargs.items():
            # set an area to be unburnable
            self.clear_spot(0, kwargs[key][0], kwargs[key][1])

    def __colour_graphics(self):
        """
        Method to colour the graphics after the simulation
        """

        for t in range(self.time):
            print(t, self.time)
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    value = self.grid[t, x, y]

                    if value == 0:
                        self.coloured_grid[t, x, y] = [0, 69, 19]
                    elif value == 1:
                        self.coloured_grid[t, x, y] = [0, 255, 0]
                    elif value == 2:
                        self.coloured_grid[t, x, y] = [255, 0, 0]
    
    def __simulate(self):
        """
        Method to start the simulation
        """

        for t in range(1, self.time):
            self.grid[t] = self.grid[t - 1].copy()
            print(t, self.time)

            for x in range(1, self.size[0] - 1):
                for y in range(1, self.size[1] - 1):

                    if self.grid[t - 1, x, y] == 2:  # if its is on fire
                        self.grid[t, x, y] = 0  # put it out and clear

                        # if there is fuel around, set on fire
                        if self.grid[t - 1, x + 1, y] == 1:
                            self.grid[t, x + 1, y] = 2
                        if self.grid[t - 1, x - 1, y] == 1:
                            self.grid[t, x - 1, y] = 2
                        # if self.grid[t - 1, x - 2, y] == 1:
                        #     self.grid[t, x - 2, y]
                        if self.grid[t - 1, x - 3, y] == 1:
                            self.grid[t, x - 3, y] = 2
                        if self.grid[t - 1, x, y + 1] == 1:
                            self.grid[t, x, y + 1] = 2
                        if self.grid[t - 1, x, y - 1] == 1:
                            self.grid[t, x, y - 1] = 2

    def __crop(self):
        """
        Crop image
        """

        self.coloured_grid = self.coloured_grid[:100, 1:self.size[0] - 1, 1:self.size[1] - 1]

    def __save_simulation(self, name: str, path: str):
        """
        Save simulation as gif
        :param name: name of file
        :param path: path to older in which to store
        """

        im.mimsave((path+f'/{name}.gif'), self.coloured_grid)



if __name__ == '__main__':

    grid = Grid(500, (300, 300), p=0.6)
    grid.clear_spot(0, (8, 100), (100, 75))
    grid.run('test', r'C:\Users\lucky\Desktop')