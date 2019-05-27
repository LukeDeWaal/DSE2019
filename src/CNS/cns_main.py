import control.matlab as cnt
import numpy as np
sys = cnt.tf([1], [1,1])
T = cnt.linspace(0,10,100)
u = np.sin(T)
(yout, Tout, xout) = cnt.lsim(sys, u, T)