# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:31:37 2019

@author: patri
"""

import numpy as np
from matplotlib import pyplot as plt
from parameters import *
from wing_surface_locations import *

#functions

def get_aerodynamic_parameters(M):
    #Inputs: Mach number 
    
    beta = np.sqrt(1-M**2)
    airfoil_efficiency = Cl_alpha/(2*np.pi/beta)
    CL_alpha_w = 2*np.pi*AR/(2 + np.sqrt(4 + (AR*beta/airfoil_efficiency)**2 * (1 + np.tan(sweep)**2)))
    CL_alpha_A_h = CL_alpha_w * (S_wing - c*hull_width)/S_wing * 1.07*(1+hull_width/b)**2
    CL_alpha_h = 2*np.pi*horizontal_tail_aspect_ratio/(2 + np.sqrt(4 + (horizontal_tail_aspect_ratio*beta/airfoil_efficiency)**2 * (1 + (np.tan(sweep)/beta)**2)))
    

    x_ac_wing = wing_position -c/2 + x_ac_airfoil * c # m
    x_ac = x_ac_wing - (1.8 * hull_width * hull_height * fus_l)/(CL_alpha_A_h * S_wing * c) + 0.273/(1 + taper_ratio) * (hull_width * S_wing/b * (b - hull_width))/(c**2 * (b + 2.15*hull_width)) * np.tan(sweep) 
    
    return CL_alpha_w, CL_alpha_A_h, CL_alpha_h, x_ac, x_ac_wing

    
CL_alpha_w=get_aerodynamic_parameters(M_stall)[0]
x_ac_wing=get_aerodynamic_parameters(M_stall)[4]
x_ac=get_aerodynamic_parameters(M_stall)[3]
Cl_alpha_h=get_aerodynamic_parameters(M_stall)[2]
CL_alpha_A_h=get_aerodynamic_parameters(M_stall)[1]




#Read file with airfoil data

f=open("NACA_6415_Cl_alpha.txt", "r")
lines=f.readlines()
angles_of_attack=[] #List of angles of attack
cl_airfoil=[] #List of lift coefficients
for line in lines:
    angles_of_attack.append(line.split(',')[0])
    cl_airfoil.append(line.replace('\t',"").split(',')[1])
f.close()

#Removes first two elements of list
angles_of_attack.pop(0)
angles_of_attack.pop(0)
cl_airfoil.pop(0)
cl_airfoil.pop(0)

#Turn the strings into integers
angles_of_attack=(list(map(float,angles_of_attack)))
cl_airfoil=(list(map(float,cl_airfoil)))

angles_of_attack=np.array(angles_of_attack)
cl_airfoil=np.array(cl_airfoil)

#Estimate of zero lift coefficient 
Cd0=0.03

#Get c_L for wing
cL_wing=np.zeros((1,len(angles_of_attack)))

alpha_zero_lift_airfoil = angles_of_attack[0]

#Get cD
cD_wing=np.zeros((1,len(angles_of_attack)))

#Here calculate cT
cT_wing=np.zeros((1,len(angles_of_attack)))

for i in range(len(angles_of_attack)):
    cL_wing[0][i]=(CL_alpha_w)*((angles_of_attack[i]-alpha_zero_lift_airfoil)*np.pi/180)

for i in range(len(angles_of_attack)):
    cD_wing[0][i]=Cd0 + cL_wing[0][i]/np.pi*AR*e
    cT_wing[0][i]=cD_wing[0][i]*np.cos(angles_of_attack[i])-cL_wing[0][i]*np.sin(angles_of_attack[i])

#get cL_max
ratio_wing_airfoil = 0.9
cl_max=max(cl_airfoil)
cL_max=cl_max*0.9

#Estimating Stall angle for wing

#The next parameter is estimated from an empirical graph
delta_alpha_cL_max = 1.2

alpha_stall = ((cL_max/CL_alpha_w))*180/np.pi +alpha_zero_lift_airfoil+delta_alpha_cL_max

#Set up new curve for cL with max angle

cL_updated=[]
for i in range(len(cL_wing[0])):
    if cL_wing[0][i]<cL_max:
        cL_updated.append(cL_wing[0][i])
cL_updated.append(cL_max)

#Get cD
cD_wing=np.zeros((1,len(cL_updated)))

#Here calculate cT
cT_wing=np.zeros((1,len(cL_updated)))
#
angles_attack_wing=[]
for i in range(len(cL_updated)):
    angles_attack_wing.append(angles_of_attack[i])
    cD_wing[0][i]=Cd0 + cL_updated[i]**2/(np.pi*AR*e)
    cT_wing[0][i]=cD_wing[0][i]*(angles_of_attack[i]*np.pi/180)-cL_updated[i]*np.sin(angles_of_attack[i]*np.pi/180)


###Get average CD_alpha
gradient_tab=[]
for j in range(len(cD_wing[0])-1):
    gradient_tab.append((cD_wing[0][j+1]-cD_wing[0][j])/(angles_attack_wing[j+1]-angles_attack_wing[j]))

cD_alpha=sum(gradient_tab)/len(gradient_tab)*(180/np.pi)

    
#Consider change in lift with different high lift devices:

triple_slotted_fowler=delta_CL_max(2.24, 0.4)


      
    

####PLOTTING####

plt.figure()
plt.plot(angles_of_attack,cL_wing[0], marker = '.', label = 'CL')
plt.plot(angles_of_attack,cl_airfoil, marker = 'v', label= 'Cl')
plt.axvline(x=alpha_stall,color='r', label = 'Stall angle wing' )
plt.axhline(y=cL_max, label = 'CL max')
plt.axhline(y=0)
plt.xlabel('alpha [deg]')
plt.ylabel('lift coefficient')
plt.title('Lift coefficient curves for airfoil and wing')
plt.legend()

plt.figure()    
plt.plot(angles_attack_wing,cT_wing[0], marker = '.' , label = 'CT')
plt.plot(angles_attack_wing,cD_wing[0], marker = 'v', label = 'CD')
plt.xlabel('alpha [deg]')
plt.title ('CD and CT')
plt.legend()

print('CL_max of the wing is', cL_max)
print('Stall angle for the wing is', alpha_stall, 'deg')






