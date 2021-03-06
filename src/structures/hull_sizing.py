import numpy as np
import matplotlib as plt
from scipy import integrate
import os

import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID

G = GoogleSheetsDataImport(SPREADSHEET_ID,'Weights', 'C&S', 'Structures')
data = G.get_data()

def step_depth_calc(L_a,beam):                          #min allowed step depth
    a = 3.4/11
    b = 2.6-3*a
    step_depth = (((L_a/beam)/a-b)/100)*beam
    step_depth_fraction = (((L_a/beam)/a-b))
    return step_depth, step_depth_fraction

def stern_post_angle_calc(x):                           #max allowed stern post angle
    a = (8.2-6)/4
    b = 8.2 - 10*a
    y= a*x+b
    return y

def dead_rise_angle_calc(H,alpha,La):                   #min allowed dead rise angle
    x = (H*alpha)/La
    a = (-10)/(0.146-0.060)
    b = 30-0.06*a
    y = a*x + b
    return y

def f_1(x,y):
    global L_Cone
    global dead_rise_angle
    global H_Cone
    return -(y/(L_Cone/(H_Cone)**2))**0.5 + np.tan(np.radians(dead_rise_angle))*x

def f_2(x,y):
    global dead_rise_angle
    global H_Cone
    return -H_Cone + np.tan(np.radians(dead_rise_angle))*x

def f_3(x,y):
    global stern_post_angle
    global step_location
    global L_Afterbody
    global step_depth
    global H_Cone
    global dead_rise_angle
    a = ((np.tan(np.radians(stern_post_angle))*L_Afterbody)-step_depth[0])/(L_Afterbody)
    b = (-H_Cone+step_depth[0])-step_location*a
    return a * y + b + np.tan(np.radians(dead_rise_angle)) * x

def bounds_y_1():
    global L_Cone
    return [0,L_Cone]

def bounds_y_2():
    global Beam_Fuselage
    global L_Cone
    return [L_Cone,1.5*Beam_Fuselage+L_Cone]

def bounds_y_3():
    global Beam_Fuselage
    global L_Cone
    global L_Afterbody
    return [L_Cone+1.5*Beam_Fuselage/2,L_Cone+1.5*Beam_Fuselage/2+L_Afterbody]

def bounds_x_1(y):
    global L_Cone
    global Beam_Fuselage
    return [0,(y/((L_Cone)/(Beam_Fuselage/2)**2))**0.5]

def bounds_x_2(y):
    global Beam_Fuselage
    return [0, Beam_Fuselage/2]

def bounds_x_3(y):
    global Beam_aft
    global Beam_Fuselage
    global L_Afterbody
    global step_location
    a = (Beam_aft/2-Beam_Fuselage/2)/L_Afterbody
    b = Beam_Fuselage/2 - a*step_location
    return [0,a*y + b]

CG = data['C&S']['CG_abs']
W_TO = data['Weights']['WTO [N]']
W_P = data['Weights']['WPL [N]']
W_F = data['Weights']['WF [N]']
L_Fuselage = data['Structures']['Max_fuselage_length']
Beam_Fuselage = data['Structures']['Max_fuselage_width']
Water_density = 1000
gravity = 9.80665
water_landing_safety = 1.8
H_Fuselage = data['Structures']['Max_fuselage_height']
CG_AC = np.subtract(CG,[1,10-H_Fuselage/2])
angle_step = np.radians(15)
H_Cone = H_Fuselage/2
Beam_aft = 0.20

step_location = CG_AC[0] + CG_AC[1]*np.tan(angle_step)
L_Afterbody = L_Fuselage - step_location
print (L_Afterbody)

step_depth = step_depth_calc(L_Afterbody, Beam_Fuselage)
print (step_depth)

stern_post_angle = stern_post_angle_calc(step_depth[1])
print (stern_post_angle)

dead_rise_angle = dead_rise_angle_calc(step_depth[0],stern_post_angle,L_Afterbody)
print (dead_rise_angle)

L_Cone = step_location - 1.5*Beam_Fuselage
print (L_Cone)

volume_cone = 2 * np.abs(integrate.nquad(f_1,[bounds_x_1,bounds_y_1])[0])
print (volume_cone)

volume_cuboid = 2 * np.abs(integrate.nquad(f_2,[bounds_x_2,bounds_y_2])[0])
print (volume_cuboid)

volume_tail = 2 * np.abs(integrate.nquad(f_3,[bounds_x_3,bounds_y_3])[0])
print (volume_tail)

volume_total = volume_cone + volume_cuboid + volume_tail

print (volume_total)




#Wing_Surface = 40.775                                   #m^2
#Wing_Span = 17.5                                        #m
#Mean_Chord = 2.33                                       #m
#Step_Location = 0.44                                    #dimensionless
#Length_Afterbody = (1 - Step_Location)*Fuselage_Length  #m
#Gravity = 9.80665                                       #m/s^2
#Water_Landing_Weight = 6000                             #kg
#Water_Landing_Safety = 1.8                              #dimensionless


