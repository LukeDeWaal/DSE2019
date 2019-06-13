import numpy as np
import matplotlib.pyplot as plt
def shear_load(F_float, w_lift, b, z, F_prop):
    if 1.3 < z <= b/2:
        Fy = -F_float - z * w_lift + (b/2) * w_lift
    if 0.75 <= z <= 1.3:
        Fy = -F_float -z*w_lift + (b/2)*w_lift - F_prop
    return Fy

g = 9.80665
F_float = 80 * g * 6.7
F_prop = 150 * g * 6.7
b = 17.48
w_lift = 36819.57447

n = 100000
z = np.linspace(0.75,b/2,n)
Fy_list = np.ones(n)
for i,j in enumerate(z):
    Fy = shear_load(F_float, w_lift, b, j, F_prop)
    Fy_list[i] = Fy

plt.clf()    
plt.plot(z,Fy_list)
plt.show()
    