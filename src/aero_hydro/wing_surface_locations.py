import matplotlib.pyplot as plt

# General paramters
MTOW = 9000 # kg
aircraft_length = 9 # m
cg_position = aircraft_length * 0.4
rho = 1.225 # kg/m^3

# Wing parameters
S = 50 # m^2
b = 19.5 # m
c = S/b # m
V_cruise = 80 # m/s
V_loit = 44 # m/s
Cl_cruise = 0.45046
Cl_loit = 2.1
L_cruise = Cl_cruise * 0.5 * rho * V_cruise**2 * S
wing_position = cg_position * 1.2
wing_moment = L_cruise * (wing_position - cg_position) # Nm

# Tail parameters
max_tail_span = 4 # m
tail_position = 8 # m
tail_force = wing_moment/(tail_position - cg_position) # N
Cl_h = -0.5
S_h = -tail_force/(Cl_h*0.5*rho*V_cruise**2)
tail_chord = S_h/max_tail_span

# Hull parameters
hull_width = 1.5 # m


def plot_forces_moments():
    # aircraft length
    plt.plot([0, aircraft_length], [0,0])
    
     # cg position
    plt.arrow(cg_position, 0, 0, -0.02, head_width=0.1, head_length=0.001)
    plt.annotate(str(round(MTOW*9.81))+' N', xy=(cg_position, -0.025))
    
     # wing position
    plt.arrow(wing_position, 0, 0, 0.02, head_width=0.1, head_length=0.001)
    plt.annotate(str(round(L_cruise))+' N', xy=(wing_position, 0.025))
    
    # tail position
    plt.arrow(tail_position, 0, 0, -0.02*tail_force/L_cruise , head_width=0.1, head_length=0.001) 
    plt.annotate(str(round(tail_force))+' N', xy=(tail_position, -0.007))
    
    plt.show()
    

#def plot_planform():
# cg
plt.plot(0, -cg_position, marker='o', markersize=3, color='red', label='CG')    
    
# hull
plt.plot([-hull_width/2, hull_width/2], [0, 0], color='k')
plt.plot([-hull_width/2, hull_width/2], [-aircraft_length, -aircraft_length], color='k')
plt.plot([-hull_width/2, -hull_width/2], [0, -aircraft_length], color='k')
plt.plot([hull_width/2, hull_width/2], [0, -aircraft_length], color='k')

# wings 
plt.plot([-b/2, b/2], [-wing_position+c/2, -wing_position+c/2], color='k')
plt.plot([-b/2, b/2], [-wing_position-c/2, -wing_position-c/2], color='k')
plt.plot([-b/2, -b/2], [-wing_position+c/2, -wing_position-c/2], color='k')
plt.plot([b/2, b/2], [-wing_position+c/2, -wing_position-c/2], color='k')

# tail
plt.plot([-max_tail_span/2, max_tail_span/2], [-tail_position+tail_chord/2, -tail_position+tail_chord/2], color='k')
plt.plot([-max_tail_span/2, max_tail_span/2], [-tail_position-tail_chord/2, -tail_position-tail_chord/2], color='k')
plt.plot([-max_tail_span/2, -max_tail_span/2], [-tail_position+tail_chord/2, -tail_position-tail_chord/2], color='k')
plt.plot([max_tail_span/2, max_tail_span/2], [-tail_position+tail_chord/2, -tail_position-tail_chord/2], color='k')


plt.axis('equal')
plt.grid()
plt.legend()
plt.show()    



def plot_cl_alpha_curve():
    plt.plot(list(range(0,21,1)), 
             [0.706, 0.796, 0.898, 0.997, 1.093, 1.188, 1.279, 1.368, 1.454, 1.534, 1.608, 1.675, 1.733, 1.780, 1.814, 1.837, 1.844, 1.838, 1.818, 1.786, 1.739])
    plt.plot([0,10], [0.706, 1.6])
    plt.xlabel('alpha')
    plt.ylabel('Cl')
    plt.grid()
    plt.show()