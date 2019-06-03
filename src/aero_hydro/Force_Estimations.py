# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:43:00 2019

@author: patri
"""

import matplotlib.pyplot as plt
import numpy as np

from wing_surface_locations import *
from parameters import *

k_paint=0.634*10**-5 #m This is a smoothness parameter depending on the surface finish
k_comp = 0.052*10**-5


######PARASITE DRAG#####
def skinfriction_drag(R,M, lt_ratio,t_c,x_c_max,sweep_angle_max,k,fuselage=True):
    
    ###Inputs###
        #R: Cruise Reynolds
        #M: Cruise Mach
        #lt_ratio: Point of turbulent transition
        #t/c: Thickness to chord ratio of the airfoil
        #x_c_max: Chordwise location of airfoil maximum thickness point
        #sweep_angle_max: Sweep of maximum thickness line (rad)
        
    
    #Wing wetted area
    S_wing_wet = 2*1.07*S_wing 
    
    #The next parameter is dependent on the type of material used in the design
    R_cutoff = 38.21*(c/k)**1.053
    
    #The lower of either the actual Reynolds or cutoff must be chosen, the cutoff gives an idea of where
    #transition occurs
    R_final = 0 
    
    if R<R_cutoff:
        R_final = R
    else:
        R_final=R_cutoff
    
    #Flat plate Skin Friction Coefficient
    #Laminar case:
    Cf_laminar = 1.328/np.sqrt(R)
    
    #Turbulence case
    Cf_turbulent = 0.455/((np.log10(R_final)**2.58)*(1+0.144*M**2)**0.65)
    
    #Based on the estimation of wing postion subjected to laminar (x_c_max)
    Cf_final=Cf_laminar*lt_ratio+Cf_turbulent*(1-lt_ratio)
        
    FF=(1+(0.6/x_c_max)*(t_c)+100*(t_c)**4)*(1.34*M**0.18*np.cos(sweep_angle_max)**0.28)
    
    Cd0 = FF*S_wing_wet*Cf_final/S_wing
    
    if fuselage:
        return 0
        
    
    return Cd0
    
print(skinfriction_drag(R_cruise_wing,M_cruise,0.2,0.16,0.4,0,k_paint,fuselage = False))


#if kwargs:
#    
#        if kwargs['fuselage']==False:
#            return 0

    
    
    




