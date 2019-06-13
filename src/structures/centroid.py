import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def line_calc(point1,point2):
    length = ((point1['x']-point2['x'])**2+(point1['y']-point2['y'])**2)**0.5
    loc_x = (point1['x']+point2['x'])/2
    loc_y = (point1['y']+point2['y'])/2
    if point2['x']-point1['x'] == 0:
        Beta = np.pi/2
    else:
        Beta = np.arctan((point2['y']-point1['y'])/(point2['x']-point1['x']))
    return length, loc_x, loc_y, Beta

def centroid_location(airfoil,tskin, tspar):
    area = 0
    x_area = 0
    y_area = 0
    for i in range(0,len(airfoil['x'])-1):
        length, loc_x, loc_y, Beta = line_calc(airfoil.iloc[i],airfoil.iloc[i+1])
        area += length*tskin
        x_area += loc_x*length*tskin
        y_area += loc_y*length*tskin
    x_centroid = x_area/area
    y_centroid = y_area/area
    return {'x': x_centroid,
            'y': y_centroid}

def inertia_calc(airfoil, centroid, tskin, tspar):
    Ixx = 0
    Iyy = 0
    Ixy = 0
    for i in range(0,len(airfoil['x'])-1):
        length, loc_x, loc_y, Beta = line_calc(airfoil.iloc[i],airfoil.iloc[i+1])
        Ixx += ((length**3)*tskin*(np.sin(Beta))**2)/12 + length * tskin * (loc_y-centroid['y'])**2
        Iyy += ((length**3)*tskin*(np.cos(Beta))**2)/12 + length * tskin * (loc_x-centroid['x'])**2
        Ixy += ((length**3)*tskin*np.sin(2*Beta))/24 + length * tskin * (loc_x-centroid['x'])*(loc_y-centroid['y'])
    return {'Ixx': Ixx,
            'Iyy': Iyy,
            'Ixy': Ixy}
#coordinates = pd.read_fwf('NACA_6415_coordinates.txt', names=['x', 'y'])*2.58
#
#
#t = 0.001
#centroid = centroid_location(coordinates, t, t)
#print (centroid)
#
#inertia = inertia_calc(coordinates, centroid, t, t)
#print (inertia)
#plt.close()
#plt.plot(coordinates['x'], coordinates['y'])
#plt.plot(centroid['x'],centroid['y'],'o')
#plt.axis('equal')
#plt.show()
