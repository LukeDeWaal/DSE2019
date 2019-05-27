import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

x = np.arange(0, 0.78, 0.01)
y = np.arange(0, 0.78, 0.01)
z = np.arange(0, 0.78, 0.01)

ax.plot_surface(x,y,z)
plt.show()

