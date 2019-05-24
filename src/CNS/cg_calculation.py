import numpy as np
import matplotlib.pyplot as plt


class CgCalculation(object):

    def __init__(self, components: dict):

        self.__components = components
        self.__cg = [None, None]
        self.calculate_cg()

    def add_component(self, name: str, weight: float, position: tuple):

        self.__components[name] = (weight, position)
        self.calculate_cg()

    def __calculate_cg_along_x(self):
        return sum([weight * position[0] for name, (weight, position) in self.__components.items()])\
               / sum([weight for name, (weight, position) in self.__components.items()])

    def __calculate_cg_along_y(self):
        return sum([weight * position[1] for name, (weight, position) in self.__components.items()])\
               / sum([weight for name, (weight, position) in self.__components.items()])

    def calculate_cg(self):
        self.__cg = [self.__calculate_cg_along_x(), self.__calculate_cg_along_y()]
        return self.__cg

    def plot_locations(self, fig: plt.figure = None):

        if fig is None:
            fig, ax = plt.subplots()
            ax.set_aspect(1.0)

        for name, (weight, (x, y)) in self.__components.items():
            plt.scatter(x, y, s=np.sqrt(weight), c='k')
            plt.annotate(name, xy=(x+0.1, y+0.1))

        plt.scatter(self.__cg[0], self.__cg[1], c='r')
        plt.annotate('CG', xy=self.__cg)

        plt.grid()
        plt.xlabel('X Position [m]')
        plt.ylabel('Y Position [m]')


if __name__ == '__main__':

    components = {
        'Fuselage': (2200, (10, 0)),
        'Wing': (800, (9, 0)),
        'Engine': (400, (14, 1)),
        'Empennage': (600, (15, 0)),
        'Payload': (4000, (12, 0))
    }

    B = CgCalculation(components)
    B.plot_locations()

