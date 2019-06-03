import numpy as np
import matplotlib as plt
from scipy import integrate

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