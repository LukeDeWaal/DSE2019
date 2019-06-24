from centroid import inertia_calc, line_calc, centroid_location
import os
import sys
import pandas as pd
import numpy as np
from decimal import Decimal

#sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

#from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID

#G = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES)
#data = G.get_data()

def area_calc(airfoil,centroid):
    area = 0
    for i in range(0,len(airfoil['x'])-1):
        line = line_calc(airfoil.iloc[i],airfoil.iloc[i+1])
        dist = shortest_distance(centroid, airfoil.iloc[i], airfoil.iloc[i+1])
        area += 0.5*dist*line[0]
#    print (area)
    return area    

def load_y_calc(w_lift, w_torque, F_float, F_prop, M_prop, chord, T_prop, b, z):
    if 2.05 < z <= b/2:
        Fy = -F_float - z * w_lift + (b/2) * w_lift
#        Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z - 1406279.463392286
        Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z - (-(((b/2)**2)*w_lift)/2 + (b/2)*w_lift*(b/2))
        Tz = w_torque*(-z+(b/2))+(-F_float*0.25*chord)
    if 0.75 <= z <= 2.05:
        Fy = -F_float - z * w_lift + (b/2) * w_lift - F_prop
#        Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z - F_prop*(-z+1.3) + M_prop - 1406279.463392286
        Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z - F_prop*(z-2.05) + M_prop - (-(((b/2)**2)*w_lift)/2 + (b/2)*w_lift*(b/2))
        Tz = w_torque*(-z+(b/2))+(-F_float*0.25*chord) + (F_prop*0.6*0.75*chord) + (T_prop*0.393)
    return {'shear':Fy,
            'moment':Mx,
            'torque':Tz}
    
def load_x_calc(w_drag, T_prop, b, z ):
    if 2.05 < z <= b/2:
        Fx = w_drag*(b/2)-w_drag*z
        My = w_drag*(b/2)*z - (w_drag/2)*z**2 - (w_drag*(b/2)*(b/2) - (w_drag/2)*(b/2)**2)
    if 0.75 <= z <= 2.05:
        Fx = w_drag*(b/2) - w_drag*z - T_prop
        My = w_drag*(b/2)*z - (w_drag/2)*z**2 - T_prop*(z-2.05) - (w_drag*(b/2)**2 - (w_drag/2)*(b/2)**2)
    return {'shear':Fx,
            'moment':My}

def normal_stress_calc(Mx, My, inertia, point, centroid):
    sigma_z = (Mx/inertia['Ixx'])*(point['y']-centroid['y'])+(My/inertia['Iyy'])*(point['x']-centroid['x'])
    return sigma_z

def shear_flow_calc(Vx, Vy, booms, inertia, centroid, point_forces, Torque):
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
    flow_torque = Torque/(2*area_encl)
    shearflows += qs_0 + flow_torque #REPHRASE
#    print (shearflows/t)
    return shearflows/t
        
def boom_calc(airfoil, inertia, t, centroid, w, b, z, w_torque, F_float, F_prop, M_prop, chord, T_prop):
    boomareas = []
    loadx = load_x_calc(w[1], T_prop, b, z)
    loady = load_y_calc(w[0], w_torque, F_float, F_prop, M_prop, chord, T_prop, b, z)
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
    von_mises_stresses = np.ones([len(booms['Area'])-1,2])
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
        von_mises_stresses[i] = (von_mises1 , von_mises2)
    return von_mises_stresses

coordinates = pd.read_fwf('Rectangular.txt', names=['x', 'y'])
coordinates.insert(loc=0, column='Area', value=0)

g = 9.80665
w_torque = 2139.32
F_float = 80 * g * 6.7
F_prop = 200 * g * 6.7
T_prop = 15000
M_prop = 2043
wing_sections = 5
AR = 7.5
wing_surface = 40.8
wing_span = np.sqrt(AR*wing_surface)
chord = wing_surface/wing_span
print (wing_span, chord)

z = (((wing_span/2)-0.75)/3)*0+0.75

t = 0.001
w = 36819.57447-(5424/(wing_span/2)), 4017.4
force_application = {'x':0.25*chord,
                     'y':0}

# centroid = centroid_location(coordinates, t, t)
# inertia = inertia_calc(coordinates, centroid, t, t)
# #print (inertia)
# #booms = boom_calc(coordinates, inertia, t, centroid, w, wing_span, z)
# booms = boom_calc(coordinates, inertia, t, centroid, w, wing_span, z, w_torque, F_float, F_prop, M_prop, chord, T_prop)
# #print (booms)
# loady = load_y_calc(w[0], w_torque, F_float, F_prop, M_prop, chord, T_prop, wing_span, z)
# loadx = load_x_calc(w[1], T_prop, wing_span, z)
# print (loady,loadx)
# print (inertia)
# shear = shear_flow_calc(loadx['shear'],loady['shear'],booms, inertia, centroid, force_application, loady['torque'])
# print (shear)
# area_calc(coordinates, centroid)
# stress = normal_stress_calc(loady['moment'], loadx['moment'], inertia, booms, centroid)
# print (stress)
weight = 0
location_wing = np.linspace(0.75, wing_span/2,wing_sections+1)
for z in location_wing[:-1]:
    #print (z)
    t = 0.001
    loady = load_y_calc(w[0], w_torque, F_float, F_prop, M_prop, chord, T_prop, wing_span, z)
    loadx = load_x_calc(w[1], T_prop, wing_span, z)
    Running = True
    while Running:
        centroid = centroid_location(coordinates, t, t)
        inertia = inertia_calc(coordinates, centroid, t, t)
        booms = boom_calc(coordinates, inertia, t, centroid, w, wing_span, z, w_torque, F_float, F_prop, M_prop, chord, T_prop)
        shear = shear_flow_calc(loadx['shear'],loady['shear'],booms, inertia, centroid, force_application, loady['torque'])
        stress = normal_stress_calc(loady['moment'], loadx['moment'], inertia, booms, centroid)
        final_stress = von_mises_stress_calc(shear,stress, booms)
        if np.max(final_stress) < 170*10**6:
            Running = False
            print (t)
            #print (final_stress)
            weight += 3.022*t*(wing_span/2)/wing_sections*2780
        t += 0.001

print (weight*2)