import numpy as np


class EulerAngles(object):

    @staticmethod
    def x_axis_rotation(theta: float):
        return np.array([[1, 0, 0],
                         [0, np.cos(theta), -np.sin(theta)],
                         [0, np.sin(theta), np.cos(theta)]])

    @staticmethod
    def y_axis_rotation(theta: float):
        return np.array([[np.cos(theta), 0, np.sin(theta)],
                         [0, 1, 0],
                         [-np.sin(theta), 0, np.cos(theta)]])

    @staticmethod
    def z_axis_rotation(theta: float):
        return np.array([[np.cos(theta), -np.sin(theta), 0],
                         [np.sin(theta), np.cos(theta), 0],
                         [0, 0, 1]])

    @classmethod
    def axis_rotation(cls, theta: float, axis: str or list or np.array):

        if type(axis) == str:
            axis = axis.lower()

        if axis == 'x' or axis == [1,0,0] or axis == np.array([1,0,0]):
            return cls.x_axis_rotation(theta)

        elif axis == 'y' or axis == [0,1,0] or axis == np.array([0,1,0]):
            return cls.y_axis_rotation(theta)

        elif axis == 'z' or axis == [0,0,1] or axis == np.array([0,0,1]):
            return cls.z_axis_rotation(theta)

        else:
            raise TypeError("Expects a string or 3-item list or array")