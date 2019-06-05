import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def centroid_location(airfoil,t):
    area = 0
    x_area = 0
    y_area = 0
    for i in range(0,len(airfoil['x'])):
        if i == len(airfoil['x'])-1:
            length = ((airfoil['x'][i]-airfoil['x'][0])**2+(airfoil['y'][i]-airfoil['y'][0])**2)**0.5
            loc_x = (airfoil['x'][i]+airfoil['x'][0])/2
            loc_y = (airfoil['y'][i]+airfoil['y'][0])/2
        else:
            length = ((airfoil['x'][i]-airfoil['x'][i+1])**2+(airfoil['y'][i]-airfoil['y'][i+1])**2)**0.5
            loc_x = (airfoil['x'][i]+airfoil['x'][i+1])/2
            loc_y = (airfoil['y'][i]+airfoil['y'][i+1])/2
        print (length, loc_x, loc_y)
        area += length*t
        x_area += loc_x*area
        y_area += loc_y*area
    x_centroid = x_area/area
    y_centroid = y_area/area
    print (x_centroid,y_centroid)
coordinates = pd.read_fwf('wingboxdimensions', names=['x', 'y'])
print (coordinates)
t = 1
centroid_location(coordinates,t)
