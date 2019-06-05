# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:31:37 2019

@author: patri
"""

import numpy as np
from matplotlib import pyplot as plt
from parameters import *

cl_alpha_airfoil=np.zeros((2,21))
cL_alpha_wing=np.zeros((2,21))

angles_of_attack = np.arange(0,21,1)

cl_alpha_airfoil[0]=angles_of_attack
cl_alpha_airfoil[1]=[0.706, 0.796, 0.898, 0.997, 1.093, 1.188, 1.279, 1.368, 1.454, 1.534, 1.608, 1.675, 1.733, 1.780, 1.814, 1.837, 1.844, 1.838, 1.818, 1.786, 1.739]

alpha_zero_lift_airfoil = -6.5

cL_alpha_wing[0]=angles_of_attack
cL_alpha_wing[1]=CL_alpha_w*((angles_of_attack-alpha_zero_lift_airfoil)*np.pi/180)

####PLOTTING####

plt.plot(cl_alpha_airfoil[0],cl_alpha_airfoil[1])
plt.plot(cL_alpha_wing[0],cL_alpha_wing[1])







