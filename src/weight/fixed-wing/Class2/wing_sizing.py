
import json
import os, pathlib
import sys
import math
sys.path.insert(0, r'C:\Users\geert\Desktop\Studie dingen\3rd year\dse\DSE2019\src\weight\fixed-wing\Class2')

class Wing_sizing(object):

    def __init__(self, name: str,taper,sweep,tc,control_surface_fraction,filepath: str = r"C:\Users\geert\Desktop\Studie dingen\3rd year\dse\DSE2019\data\Class II Data",datadict: dict = {}):
        self.__name = name
        self.__fp = filepath + f'\\{self.__name}_estimate.json'
        self.__datadict = datadict

        self.__full_data = dict()
        self.__data = dict()

        self.__read_from_json()

        # self.__wing_weight = self.wing_weight()
        self.taper = taper
        self.sweep = sweep
        self.tc = tc
        self.control_surface_fraction = control_surface_fraction

    def getdata(self):
        return self.__data

    def __read_from_json(self):

        with open(self.__fp, 'r') as file:
            self.__full_data = json.load(file)

        try:
            self.__data = self.__full_data

        except KeyError:
            return


    def wing_weight(self):
        load_factor = 4.4
        wto = self.__data['2000L']['weights']['wto']
        Sw = self.__data['2000L']['wing']['area']
        Aspect = self.__data['2000L']['wing']['AR']
        control_surface = Sw*self.control_surface_fraction
        weight = 0.0051*9((wto+load_factor)**0.557)*(Sw**0.649)*(Aspect**0.5)*(self.tc**-0.4)*((1+self.taper)**0.1)*(math.cos(self.taper)**-1)*control_surface**0.1
        return weight

wing_weight_object = Wing_sizing('twin_engine',0.3,0,0.3,0.2)
# print(wing_weight_object.wing_weight())

a = wing_weight_object.getdata()



#def wing_weight(tc,taper,sweep,control_surface):
