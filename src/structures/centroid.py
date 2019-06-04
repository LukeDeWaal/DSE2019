import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def centroid_location(airfoil):
    for i in range(0,len(airfoil['x'])):
        if i < 3:
            length = ((airfoil['x'][i]-airfoil['x'][i+1])**2+(airfoil['y'][i]-airfoil['y'][i+1])**2)**0.5
            print (length)

coordinates = pd.read_fwf('wingboxdimensions', names=['x', 'y'])
centroid_location(coordinates)
