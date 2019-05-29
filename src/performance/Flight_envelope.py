import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})

MTOW = 8525                     #kg
g = 9.80665                     #m/s2
S = 47.35                       #m2
CLmax = 2.8
CL_clean = 1.489
CLmin = -0.8 * CL_clean
rho = 1.225                     #kg/m3
n_max = 4.4
n_min = -1
V_cruise = 80                   #m/s

Wing_loading = (MTOW*g)/(S)     #N/m2
print (Wing_loading)

V_cruise_min = 33*np.sqrt(0.02088547)*0.5144444*np.sqrt(Wing_loading) #m/s
print (V_cruise_min)

V_A = np.sqrt((2*n_max*Wing_loading)/(rho*CLmax))
print (V_A)

V_Stall = np.sqrt((2*Wing_loading)/(rho*CLmax))
print (V_Stall)

V_neg = np.sqrt((2*n_min*Wing_loading)/(rho*CLmin))

V_takeoff_curve = np.linspace(0, V_A, num=100)
n_takeoff_curve = (0.5*rho*V_takeoff_curve**2*CLmax)/Wing_loading

V_neg_curve = np.linspace(0,V_neg, num=100)
n_neg_curve = (0.5*rho*V_neg_curve**2*CLmin)/Wing_loading

V_D = 1.4 * V_cruise_min

n_pos = [n_max,n_max]
n_vert = [n_max,0]
V_diag = [V_cruise_min,V_D]
n_diag = [n_min,0]
V_neg = [V_neg,V_cruise_min]
n_neg = [n_min,n_min]
StallV = [0,V_D]

plt.plot(V_takeoff_curve,n_takeoff_curve,'blue')
plt.plot(V_neg_curve,n_neg_curve,'blue')
plt.plot([V_A,V_D],n_pos,'blue')
plt.plot([V_D,V_D],n_vert,'blue')
plt.plot(V_diag,n_diag,'blue')
plt.plot(V_neg,n_neg,'blue')
plt.plot(StallV,[1,1],'--',color='black')
plt.plot([V_A,V_A],[n_max,0],'--',color='black')
plt.plot([V_cruise_min,V_cruise_min],[n_min,0],'--',color='black')
plt.axhline(0, color='black')
plt.xlabel('V (m/s)')
plt.ylabel('n')
plt.show()