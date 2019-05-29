import numpy as np
import matplotlib.pyplot as plt


class CgCalculation(object):

    def __init__(self, components: dict):
        """
        Object to calculate the centre of gravity in 3 Dimensions for any system
        :param components: {
                    component: (weight, (x, z)),
                    ...
                    }
        """

        self.__components = components
        self.__cg = [None, None]
        self.__cg_lemac = [None, None]
        self.calculate_cg()
        # self.cg_xlemac()

    def add_component(self, name: str, weight: float, position: tuple):
        """
        Add Component to the calculation
        :param name: Component Name
        :param weight: Component Weight
        :param position: Component position in (x, z)
        :return:
        """

        self.__components[name] = (weight, position)
        self.calculate_cg()

    def __calculate_cg_along_x(self):
        """
        Calculate X coordinate of CG
        :return:
        """
        return sum([weight * position[0] for name, (weight, position) in self.__components.items()])\
               / sum([weight for name, (weight, position) in self.__components.items()])

    def __calculate_cg_along_z(self):
        """
        Calculate Z coordinate of CG
        :return:
        """
        return sum([weight * position[1] for name, (weight, position) in self.__components.items()])\
               / sum([weight for name, (weight, position) in self.__components.items()])

    def calculate_cg(self):
        """
        Calculate x, z position of CG
        :return:
        """
        self.__cg = [self.__calculate_cg_along_x(), self.__calculate_cg_along_z()]
        return self.__cg

    def cg_xlemac(self, d_xlemac: float):
        """
        Calculate CG in XLEMAC coordinates
        :param d_xlemac: Distance from nose tip to XLEMAC
        :return:
        """
        self.__cg_lemac = [self.__cg[0] - d_xlemac, self.__cg[1]]
        return self.__cg_lemac

    @staticmethod
    def __plot_cilinder(length: float, height: float, offset: tuple = (0, 0)):

        height = height/2
        xdata = []
        ydata = []

        # First Circular Part
        for theta in np.linspace(0, np.pi/2, 10):
            xdata.append(height - np.cos(theta)*height)
            ydata.append(np.sin(theta)*height)

        # Straight Part
        for xi in np.linspace(height, length-height, 100):
            xdata.append(xi)
            ydata.append(height)

        # Second Circular Part
        for theta in np.linspace(np.pi/2, 0, 10):
            xdata.append(length - height + np.cos(theta)*height)
            ydata.append(np.sin(theta)*height)

        bottom_x = []
        bottom_y = []

        for xi, yi in zip(xdata[::-1], ydata[::-1]):
            bottom_x.append(xi)
            bottom_y.append(-yi)

        xdata.extend(bottom_x)
        ydata.extend(bottom_y)

        return np.array(xdata) + offset[0], np.array(ydata) + offset[1]

    def plot_locations(self, fig: plt.figure = None):
        """
        Make a component plot of all components and weights
        :param fig: fig to plot in
        :return:
        """

        if fig is None:
            fig, ax = plt.subplots()
            ax.set_aspect(1.0)

        for name, (weight, (x, z)) in self.__components.items():
            plt.scatter(x, z, s=np.sqrt(weight), c='k')
            plt.annotate(name, xy=(x+0.1, z+0.1))

        plt.scatter(self.__cg[0], self.__cg[1], c='r')
        plt.annotate('CG', xy=self.__cg)

        # fuselage = self.__plot_cilinder(9, 2.5)
        # wing = self.__plot_cilinder(2.6, 0.2, offset=(3,1.5))
        #
        # plt.plot(fuselage[0], fuselage[1])
        # plt.plot(wing[0], wing[1])

        plt.grid()
        plt.xlabel('X Position [m]')
        plt.ylabel('Y Position [m]')


if __name__ == '__main__':

    components = {
        'Fuselage': (2200, (5, 0)),
        'Wing': (800, (3, 1.5)),
        'Engine': (400, (6, 2.0)),
        'Empennage': (600, (9, 2.0)),
        'Payload': (4000, (4, 0)),
        'Fuel': (200, (3, 1.5))
    }

    B = CgCalculation(components)
    B.plot_locations()

