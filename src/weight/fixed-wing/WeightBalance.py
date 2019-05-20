import numpy as np
import matplotlib.pyplot as plt


class CG_Calculation(object):

    def __init__(self, weight_list: list, x_position_list: list, y_position_list: list = None):

        self.__weights = weight_list
        self.__x_positions = x_position_list

        if y_position_list is None:
            self.__y_positions = [0]*len(x_position_list)

        else:
            self.__y_positions = y_position_list

    def add_component(self, weight: float, position: tuple):

        self.__weights.append(weight)
        self.__x_positions.append(position[0])
        self.__y_positions.append(position[1])

    def calculate_cg_along_x(self):
        return sum([weight * position for weight, position in zip(self.__weights, self.__x_positions)]) / sum(self.__weights)

    def calculate_cg_along_y(self):
        return sum([weight * position for weight, position in zip(self.__weights, self.__y_positions)]) / sum(self.__weights)

    def plot_locations(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        plt.scatter(self.__x_positions, self.__y_positions, s=self.__weights)
        plt.grid()
        plt.xlabel('X Position [m]')
        plt.ylabel('Y Position [m]')


if __name__ == '__main__':

    B = CG_Calculation([100, 100, 200], [0, 10, 15.5], [0, 0, 0.5])
    B.plot_locations()
    print(B.calculate_cg_along_x())
    print(B.calculate_cg_along_y())
    B.add_component(150, (2, 0))
    print(B.calculate_cg_along_x())
    print(B.calculate_cg_along_y())