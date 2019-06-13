from centroid import inertia_calc, line_calc, centroid_location
import os
import sys
import pandas as pd
import numpy as np
from decimal import Decimal

sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID

G = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES)
data = G.get_data()

def area_calc(airfoil,centroid):
    area = 0
    for i in range(0,len(airfoil['x'])-1):
        line = line_calc(airfoil.iloc[i],airfoil.iloc[i+1])
        dist = shortest_distance(centroid, airfoil.iloc[i], airfoil.iloc[i+1])
        area += 0.5*dist*line[0]
    return area    

def load_calc(w, b, z):
    shear = w*(b/2-z)
    moment = (w*b/2)*z - ((w*z**2)/2) - ((w*b**2)/8)
    return {'shear':shear,
            'moment':moment}

def normal_stress_calc(Mx, My, inertia, point, centroid):
    sigma_z = (Mx/inertia['Ixx'])*(point['y']-centroid['y'])+(My/inertia['Iyy'])*(point['x']-centroid['x'])
    return sigma_z

def shear_flow_calc(Vx, Vy, booms, inertia, centroid, point_forces):
    boom_term_y = booms['Area']*(booms['y']-centroid['y'])
    boom_term_x = booms['Area']*(booms['x']-centroid['x'])
    inertia_term_y = Vy/inertia['Ixx']
    inertia_term_x = Vx/inertia['Iyy']
    #print (inertia_term_y*boom_term_y[0])
    shear_base = -(Vy/inertia['Ixx'])*booms['Area']*(booms['y']-centroid['y'])-(Vx/inertia['Iyy'])*booms['Area']*(booms['x']-centroid['x'])
    #print (shear_base)
    area_encl = area_calc(booms, centroid)
    temp_moment = 0
    shearflows = np.ones([len(shear_base)-1,1])
    for i,j in enumerate(shear_base[:-1]):
        shearflow = sum(shear_base[:i+1])
        shearflows[i] = shearflow
        line = line_calc(booms.iloc[i],booms.iloc[i+1])
        dist = shortest_distance(point_forces, booms.iloc[i], booms.iloc[i+1])
        temp_moment += shearflow*line[0]*dist
    qs_0 = -(temp_moment/(2*area_encl))
    #print (shearflows)
    #print (qs_0)
    shearflows += qs_0
#    print (shearflows/t)
    return shearflows/t
        
def boom_calc(airfoil, inertia, t, centroid, w, b, z):
    boomareas = []
    loadx = load_calc(w[0],b,z)
    loady = load_calc(w[1],b,z)
    for i in range(0, len(airfoil['x'])-1):
        if i == 0:
            line = line_calc(airfoil.iloc[i],airfoil.iloc[i+1])
            line2 = line_calc(airfoil.iloc[i],airfoil.iloc[i-2])
            stress = normal_stress_calc(loadx['moment'], loady['moment'], inertia, airfoil.iloc[i],centroid)
            stress_next = normal_stress_calc(loadx['moment'], loady['moment'], inertia, airfoil.iloc[i+1],centroid)
            stress_prev = normal_stress_calc(loadx['moment'], loady['moment'], inertia, airfoil.iloc[i-2],centroid)
            boom_area = (t*line[0]/6)*(2+(stress_next/stress))+(t*line2[0]/6)*(2+(stress_prev/stress))
            boomareas.append(boom_area)
            
        else:    
            line = line_calc(airfoil.iloc[i],airfoil.iloc[i+1])
            line2 = line_calc(airfoil.iloc[i],airfoil.iloc[i-1])
            stress = normal_stress_calc(loadx['moment'], loady['moment'], inertia, airfoil.iloc[i],centroid)
            stress_next = normal_stress_calc(loadx['moment'], loady['moment'], inertia, airfoil.iloc[i+1],centroid)
            stress_prev = normal_stress_calc(loadx['moment'], loady['moment'], inertia, airfoil.iloc[i-1],centroid)
            boom_area = (t*line[0]/6)*(2+(stress_next/stress))+(t*line2[0]/6)*(2+(stress_prev/stress))
            boomareas.append(boom_area)
    boomareas.append(boomareas[0])
    airfoil['Area'] = boomareas
    return airfoil

def shortest_distance(point, line_point1, line_point2):
    a = line_point1['y']-line_point2['y']
    b = line_point2['x']-line_point1['x']
    c = line_point1['x']*line_point2['y'] - line_point2['x']*line_point1['y']
    d = abs((a * point['x'] + b * point['y'] + c)) / (np.sqrt(a * a + b * b)) 
    return d

def von_mises_stress_calc(shearstresses, normal_stresses, booms):
    unit_vectors = np.ones([len(booms['Area'])-1,2])
    stresses = np.ones([len(booms['Area'])-1,1])
    von_mises_stresses = np.ones([len(booms['Area'])-1,1])
    for i in range(len(booms['Area'])-1):
        vector = -np.array([booms['x'][i],booms['y'][i]]) + np.array([booms['x'][i + 1],booms['y'][i + 1]])
        unit = vector/np.linalg.norm(vector)
        unit_vectors[i] = unit
    #dis_shear = unit_vectors*shearstresses
    for i in range(len(booms['Area'])-1):
        #shear_boom = dis_shear[i] + dis_shear[i-1]
        #print (shear_boom)
        von_mises1 = (normal_stresses[i]**2 + 3*shearstresses[i]**2)**0.5
        von_mises2 = (normal_stresses[i]**2 + 3*shearstresses[i-1]**2)**0.5
        #print ("{:.3E}".format(Decimal(von_mises)))
        von_mises_stresses[i] = (von_mises1 + von_mises2)/2
    return von_mises_stresses

coordinates = pd.read_fwf('Rectangular.txt', names=['x', 'y'])
coordinates.insert(loc=0, column='Area', value=0)

wing_span = 17.48
chord = 2.33
t = 0.0005
w = 33600.93, 4017.4
force_application = {'x':0.25*chord,
                     'y':0}

centroid = centroid_location(coordinates, t, t)
inertia = inertia_calc(coordinates, centroid, t, t)
#print (inertia)
booms = boom_calc(coordinates, inertia, t, centroid, w, wing_span, 5)
#print (booms)
loady = load_calc(w[0],wing_span,0)
loadx = load_calc(w[1],wing_span,0)
print (loady)
print (inertia)
shear = shear_flow_calc(loadx['shear'],loady['shear'],booms, inertia, centroid, force_application)
print (shear)
area_calc(coordinates, centroid)
stress = normal_stress_calc(loady['moment'], loadx['moment'], inertia, booms, centroid)
print (stress)

Running = True
while Running:
    centroid = centroid_location(coordinates, t, t)
    inertia = inertia_calc(coordinates, centroid, t, t)
    booms = boom_calc(coordinates, inertia, t, centroid, w, wing_span, 5)
    shear = shear_flow_calc(loadx['shear'],loady['shear'],booms, inertia, centroid, force_application)
    stress = normal_stress_calc(loady['moment'], loadx['moment'], inertia, booms, centroid)
    final_stress = von_mises_stress_calc(shear,stress, booms)
    if np.max(final_stress) < 241*10**6:
        Running = False
        print (t)
        print (final_stress)
    t += 0.0005
    
    
