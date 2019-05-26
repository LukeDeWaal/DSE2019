import json
import os, pathlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

# sys.path.insert(0, r'C:\Users\geert\Desktop\Studie dingen\3rd year\dse\DSE2019\src\weight\fixed-wing\Class2')


class Wing_sizing(object):

    def __init__(self, name: str,filepath: str = r"C:\Users\LRdeWaal\Desktop\DSE2019\data\Class II Data", **kwargs):

        self.__name = name
        self.__fp = filepath + f'\\{self.__name}_estimate.json'

        self.__full_data = dict()
        self.__data = dict()

        self.__read_from_json()
        self.__weights = {key: None for key in self.__data.keys()}

        try:
            self.__taper = kwargs['taper']
            self.__sweep = kwargs['sweep']
            self.__tc = kwargs['tc']
            self.__Sc = kwargs['Sc']

        except KeyError:
            print("No Values Provided")
            quit()

        self.wing_weight()

    def getdata(self):
        return self.__data

    def get_weights(self):
        return self.__weights

    def __read_from_json(self):

        with open(self.__fp, 'r') as file:
            self.__full_data = json.load(file)

        try:
            self.__data = self.__full_data

        except KeyError:
            return

    @staticmethod
    def __wing_weight(wto, nz, Sw, Sc, AR, tc, taper, sweep):
        return 0.0051*((wto * nz)**(0.557))*(Sw**(0.649))*(AR**(0.5))*((tc)**(-0.4))*((1+taper)**(0.1))*((np.cos(sweep))**(-1.0))*(Sc**(0.1))

    def wing_weight(self):
        n_max = 4.4

        for key, value in self.__data.items():

            WTO = self.__data[key]['weights']['wto']*9.80665
            AR = self.__data[key]['wing']['AR']
            Sw = self.__data[key]['wing']['area']

            weight = self.__wing_weight(wto=WTO, AR=AR, Sw=Sw, nz=n_max, Sc=self.__Sc*Sw, taper=self.__taper, sweep=self.__sweep, tc=self.__tc)
            self.__weights[key] = weight



wing_weight_object = Wing_sizing('twin_engine', filepath=r"C:\Users\LRdeWaal\Desktop\DSE2019\data\Class II Data", sweep=5*np.pi/180, taper=1, tc=0.1, Sc=0.14)
# print(wing_weight_object.wing_weight())

a = wing_weight_object.get_weights()



#def wing_weight(tc,taper,sweep,control_surface):
