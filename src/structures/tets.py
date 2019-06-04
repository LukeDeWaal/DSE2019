#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:19:12 2019

@author: liesbethwijn
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from parameters import *

def plot_naca_6415():
    coordinates = pd.read_fwf('NACA_6415_coordinates.txt', names=['x', 'y'])
    print(coordinates)
    plt.plot(coordinates['x'], coordinates['y'])
    plt.axis('equal')
    plt.grid()
    plt.show()
  
plot_naca_6415()
