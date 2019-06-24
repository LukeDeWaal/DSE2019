import numpy as np
import matplotlib.pyplot as plt

def shear_load_calc(F_float, w_lift, b, z, F_prop):
    if 2.05 < z <= b/2:
        Fy = -F_float - z * w_lift + (b/2) * w_lift
    if 0.75 <= z <= 2.05:
        Fy = -F_float -z*w_lift + (b/2)*w_lift - F_prop
    return Fy

def moment_calc(F_float, w_lift, b, F_prop, M_prop, z):
    if 2.05 < z <= b/2:
#        Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z - 1382576.583392286
#         Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z - 1245099.8793922865
        Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z -(-(((b/2)**2)*w_lift)/2 + (b/2)*w_lift*(b/2))
    if 0.75 <= z <= 2.05:
#        Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z - F_prop*(z-2.05) + M_prop - 1382576.583392286
#         Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z - F_prop*(z-2.05) + M_prop - 1245099.8793922865
        Mx = -F_float*(z-(b/2))-((z**2)*w_lift)/2 + (b/2)*w_lift*z - F_prop*(z-2.05) + M_prop -(-(((b/2)**2)*w_lift)/2 + (b/2)*w_lift*(b/2))
    return Mx

def torque_calc(w_torque, z, b, F_float, F_prop, chord, T_prop):
    if 2.05 < z <= b/2:
        Tz = w_torque*(-z+(b/2))+(-F_float*0.25*chord)
    if 0.75 <= z <= 2.05:
        Tz = w_torque*(-z+(b/2))+(-F_float*0.25*chord) + (F_prop*0.6*0.75*chord) + (T_prop*0.393)
    return Tz

def load_x_calc(w_drag, T_prop, b, z):
    if 2.05 < z <= b/2:
        Fx = w_drag*(b/2)-w_drag*z
        My = w_drag*(b/2)*z - (w_drag/2)*z**2 - (w_drag*(b/2)*(b/2) - (w_drag/2)*(b/2)**2)
    if 0.75 <= z <= 2.05:
        Fx = w_drag*(b/2) - w_drag*z - T_prop
        My = w_drag*(b/2)*z - (w_drag/2)*z**2 - T_prop*(z-2.05) - (w_drag*(b/2)*(b/2) - (w_drag/2)*(b/2)**2)
    return Fx,My

g = 9.80665
AR = 7.5
wing_surface = 40.8
b = np.sqrt(AR*wing_surface)
print (b)
chord = wing_surface/b
F_float = 80 * g * 6.7
#F_float = 0
F_prop = 200 * g * 6.7
#F_prop = 0
#b = 17.48
#w_lift = 3689.57447
w_lift = 36819.57447-(5424/(b/2))
M_prop = 2043
#M_prop = 0
T_prop = 15000
w_torque = 2139.32
w_drag = 4017.4

n = 100000
z = np.linspace(0.75,b/2,n)
Fy_list = np.ones(n)
Mx_list = np.ones(n)
Tz_list = np.ones(n)
Fx_list = np.ones(n)
My_list = np.ones(n)
for i,j in enumerate(z):
    Fy = shear_load_calc(F_float, w_lift, b, j, F_prop)
    Mx = moment_calc(F_float, w_lift, b, F_prop, M_prop, j)
    Tz = torque_calc(w_torque, j, b, F_float, F_prop, chord, T_prop)
    Fx, My = load_x_calc(w_drag, T_prop, b, j)
    Fy_list[i] = Fy
    Mx_list[i] = Mx
    Tz_list[i] = Tz
    Fx_list[i] = Fx
    My_list[i] = My

print (Mx_list[-1])

print (moment_calc(F_float, w_lift, b, F_prop, M_prop, 0.75))

colours = [  # Use these colours to cycle through if you want to plot multiple lines in the same plot
   (255 / 255, 0, 0),
   (107 / 255, 142 / 255, 35 / 255),
   (30 / 255, 144 / 255, 255 / 255),
   (0, 0, 139 / 255),
   (255 / 255, 165 / 255, 0),
   (34 / 255, 139 / 255, 34 / 255)
]
line_types = ['-', '--']  # Choose one of these linetypes
marker_types = ['.', 'o', 'x']  # In case markers are desired, use one of these
data = [z, My_list]  # Replace with our data sets
plot_label = 'Mx'  # Set the desired label
axis_labels = ['z [m]', 'Mx [Nm]']  # Set the axis labels
axis_ranges = [(0, b/2), (-1200000, 20000)]  # Set the axis ranges
plot_title = 'Moment diagram around the x-axis'

fig = plt.figure()
plt.plot(data[0], data[1], c=colours[1], label=plot_label)
plt.xlim(axis_ranges[0][0], axis_ranges[0][1])
#plt.ylim(axis_ranges[1][0], axis_ranges[1][1])
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend()
plt.xlabel(axis_labels[0], fontsize=16)
plt.ylabel(axis_labels[1], fontsize=16)
plt.title(plot_title, fontsize=18)
plt.show()