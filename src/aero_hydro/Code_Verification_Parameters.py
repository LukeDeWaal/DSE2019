# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 09:23:54 2019

@author: patri
"""

import numpy as np

###These parameters have been taken from a Raymer design example for a single seat aerobatic hombebuilt aicraft. 
### It may be useful to use them for code verification


#GERNERAL PARAMTERS#
Vcruise = 56.6
Mcruise=0.15
rho_cruise=1.225
miu_cruise=1.789*10**-5

#WING PARAMETERS#
AR_wing=6.
taper_wing = 0.4
t_c_wing=0.15
c_wing=1.42

#TAIL PARAMETERS#
AR_horizontal= 4.
taper_horizontal = 0.4
span_horizontal=3.08
area_horizontal=2.37
t_c_tail = 0.12
c_tail=0.85

AR_vertical =4.
taper_vertical = 0.4
span_vertical=1.25
area_vertical = 1.08

S_ref_ray= 11.
fus_length=6.7

#ENGINE PARAMETERS#
propeller_diam = 1.96

#GEAR
tire_width = 0.135
tire_diam = 0.279

#Reynolds numbers

Reynolds_wing= rho_cruise*c_wing*Vcruise/miu_cruise
Reynolds_tail= rho_cruise*c_tail*Vcruise/miu_cruise
Reynolds_fus= rho_cruise*fus_length*Vcruise/miu_cruise



