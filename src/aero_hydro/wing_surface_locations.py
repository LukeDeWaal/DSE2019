import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from parameters import *
from Control_Coefficients import *



def plot_forces_moments():
    """
    Plots the positions of the CG, lift of the wing and lift of the tail with their respective forces
    """
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
    

def plot_planform():
    """
    Plots the planform of the aircraft
    """
    CL_alpha_w, CL_alpha_A_h, CL_alpha_h, x_ac, x_ac_wing = get_aerodynamic_parameters(mach)
    
    # top view
    plt.subplot(2,1,1)

    # top_view = {
    #     'hull': [
            
    #     ],
    #     'wings': [
    #         [-b/2, b/2], [-wing_position+c/2, -wing_position+c/2],
    #     ]
    #     'vertical_tail': [
    #         [fus_l-vertical_tail_root_chord, hull_height/2],
    #         [fus_l-vertical_tail_tip_chord, hull_height/2+vertical_tail_height],
    #         [fus_l, hull_height/2+vertical_tail_height],
    #         [fus_l, hull_height/2] 
    #     ],
    #     'airfoil': airfoil_coordinates,
    # }
    
    # CG
    plt.plot(0, -cg_position, marker='o', markersize=3, color='red', label='Center of Gravity') 
     
    # center of pressure
    plt.plot(0, -x_ac, marker='o', markersize=3, color='blue', label='Center of Pressure') 
        
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
    plt.plot([-max_tail_span/2, max_tail_span/2], [-tail_position+horizontal_tail_chord/2, -tail_position+horizontal_tail_chord/2], color='k')
    plt.plot([-max_tail_span/2, max_tail_span/2], [-tail_position-horizontal_tail_chord/2, -tail_position-horizontal_tail_chord/2], color='k')
    plt.plot([-max_tail_span/2, -max_tail_span/2], [-tail_position+horizontal_tail_chord/2, -tail_position-horizontal_tail_chord/2], color='k')
    plt.plot([max_tail_span/2, max_tail_span/2], [-tail_position+horizontal_tail_chord/2, -tail_position-horizontal_tail_chord/2], color='k')
    
    # control surface
    plt.plot([-0.9*b/2, -0.9*b/2+aileron_length], [-wing_position-c/2+aileron_chord, -wing_position-c/2+aileron_chord], color='k')
    plt.plot([-0.9*b/2, -0.9*b/2], [-wing_position-c/2+aileron_chord, -wing_position-c/2], color='k')
    plt.plot([-0.9*b/2+aileron_length, -0.9*b/2+aileron_length], [-wing_position-c/2+aileron_chord, -wing_position-c/2], color='k')
    
    plt.plot([0.9*b/2, 0.9*b/2-aileron_length], [-wing_position-c/2+aileron_chord, -wing_position-c/2+aileron_chord], color='k')
    plt.plot([0.9*b/2, 0.9*b/2], [-wing_position-c/2+aileron_chord, -wing_position-c/2], color='k')
    plt.plot([0.9*b/2-aileron_length, 0.9*b/2-aileron_length], [-wing_position-c/2+aileron_chord, -wing_position-c/2], color='k')
    
    plt.plot([-elevon_length/2, elevon_length/2], [-tail_position-horizontal_tail_chord/2+elevon_chord, -tail_position-horizontal_tail_chord/2+elevon_chord], color='k')
    plt.plot([-elevon_length/2, -elevon_length/2], [-tail_position-horizontal_tail_chord/2+elevon_chord, -tail_position-horizontal_tail_chord/2], color='k')
    plt.plot([elevon_length/2, elevon_length/2], [-tail_position-horizontal_tail_chord/2+elevon_chord, -tail_position-horizontal_tail_chord/2], color='k')

    plt.axis('scaled')
    plt.grid()
    plt.legend()  
    
    
    # side view
    plt.subplot(2, 1, 2)
    
    airfoil_coordinates = pd.read_fwf('NACA_6415_coordinates.txt', names=['x', 'y']) * c
    airfoil_coordinates['x'] += wing_position - c/2
    airfoil_coordinates['y'] += hull_height/2 - 0.1 * c
        
    side_view = {
        'hull': [
            [0, -hull_height/2],
            [0, hull_height/2],
            [fus_l, hull_height/2],
            [fus_l, -hull_height/2],  
        ],
        'vertical_tail': [
            [fus_l-vertical_tail_root_chord, hull_height/2],
            [fus_l-vertical_tail_tip_chord, hull_height/2+vertical_tail_height],
            [fus_l, hull_height/2+vertical_tail_height],
            [fus_l, hull_height/2] 
        ],
        'airfoil': airfoil_coordinates,
    }
    for component in side_view.values():
        plt.gca().add_patch(plt.Polygon(component, fill=None, linewidth=1.5))
    
    
    
    
    
    plt.axis('scaled')
    plt.grid()
    plt.show()  


def plot_cl_alpha_curve():
    """
    Plots the Cl-alpha curve, of the NACA 6415, based on JavaFoil
    """
    data = pd.read_csv('NACA_6415_Cl_alpha.txt', skiprows=2, names=['alpha', 'Cl', 'Cd' , 'Cm0.25', 'Cp', 'M_cr'])
    
    colours = [  # Use these colours to cycle through if you want to plot multiple lines in the same plot
   (255 / 255, 0, 0),
   (255 / 255, 165 / 255, 0),
   (132 / 255, 198 / 255, 0 / 255),
   (30 / 255, 144 / 255, 255 / 255),
   (0, 0, 139 / 255),
   (193 / 255, 38 / 255, 144 / 255)
   ]
    
    line_types = ['-', '--']  # Choose one of these linetypes
    marker_types = ['.', 'o', 'x']  # In case markers are desired, use one of these
    data = [data['alpha'], data['Cl']]  # Replace with our data sets
    #plot_label = 'label'  # Set the desired label
    axis_labels = ['alpha [deg]', 'Cl [-]']  # Set the axis labels
    #axis_ranges = [(0, 3), (0, 5)]  # Set the axis ranges
    plot_title = 'Cl-alpha curve'
    
    fig = plt.figure()
    plt.plot(data[0], data[1], f'{line_types[0]}', c=colours[1])#, label=plot_label)
    #plt.xlim(axis_ranges[0][0], axis_ranges[0][1])
    #plt.ylim(axis_ranges[1][0], axis_ranges[1][1])
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    #plt.legend()
    plt.xlabel(axis_labels[0], fontsize=16)
    plt.ylabel(axis_labels[1], fontsize=16)
    plt.axhline(color='k')
    plt.axvline(color='k')
    plt.title(plot_title, fontsize=18)

       
    
def plot_naca_6415():
    coordinates = pd.read_fwf('NACA_6415_coordinates.txt', names=['x', 'y'])
    plt.plot(coordinates['x'], coordinates['y'])
    plt.axis('equal')
    plt.grid()
    plt.show()
    
    
def delta_CL_max(Cl_max_flaps, Cl_max_slats):
    S_flapped = 4*c * 2  
    S_slatted = 7*c * 2
    delta_CL_max = 0.9 * (Cl_max_flaps*S_flapped/S_wing + Cl_max_slats*S_slatted/S_wing) * np.cos(np.deg2rad(0))
    return delta_CL_max

def plot_cm_alpha_curve():
    data = pd.read_csv('NACA_6415_Cl_alpha.txt', skiprows=2, names=['alpha', 'Cl', 'Cd' , 'Cm0.25', 'Cp', 'M_cr'])
    
    colours = [  # Use these colours to cycle through if you want to plot multiple lines in the same plot
   (255 / 255, 0, 0),
   (255 / 255, 165 / 255, 0),
   (132 / 255, 198 / 255, 0 / 255),
   (30 / 255, 144 / 255, 255 / 255),
   (0, 0, 139 / 255),
   (193 / 255, 38 / 255, 144 / 255)
   ]
    
    line_types = ['-', '--']  # Choose one of these linetypes
    marker_types = ['.', 'o', 'x']  # In case markers are desired, use one of these
    data = [data['alpha'], data['Cm0.25']]  # Replace with our data sets
    #plot_label = 'label'  # Set the desired label
    axis_labels = ['alpha [deg]', 'Cm [-]']  # Set the axis labels
    axis_ranges = [(-3, 20), (0, 5)]  # Set the axis ranges
    plot_title = 'Cm-alpha curve'
    
    fig = plt.figure()
    plt.plot(data[0], data[1], f'{line_types[0]}', c=colours[1])#, label=plot_label)
    plt.xlim(axis_ranges[0][0], axis_ranges[0][1])
    #plt.ylim(axis_ranges[1][0], axis_ranges[1][1])
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    #plt.legend()
    plt.xlabel(axis_labels[0], fontsize=16)
    plt.ylabel(axis_labels[1], fontsize=16)
    plt.axhline(color='k')
    plt.axvline(color='k')
    plt.title(plot_title, fontsize=18)
    
def plot_cl_cd_curve():
    data = pd.read_csv('NACA_6415_Cl_alpha.txt', skiprows=2, names=['alpha', 'Cl', 'Cd' , 'Cm0.25', 'Cp', 'M_cr'])
    
    colours = [  # Use these colours to cycle through if you want to plot multiple lines in the same plot
   (255 / 255, 0, 0),
   (255 / 255, 165 / 255, 0),
   (132 / 255, 198 / 255, 0 / 255),
   (30 / 255, 144 / 255, 255 / 255),
   (0, 0, 139 / 255),
   (193 / 255, 38 / 255, 144 / 255)
   ]
    
    line_types = ['-', '--']  # Choose one of these linetypes
    marker_types = ['.', 'o', 'x']  # In case markers are desired, use one of these
    data = [data['Cd'], data['Cl']]  # Replace with our data sets
    #plot_label = 'label'  # Set the desired label
    axis_labels = ['Cd [-]', 'Cl [-]']  # Set the axis labels
    axis_ranges = [(-3, 20), (0, 5)]  # Set the axis ranges
    plot_title = 'Cl-Cd curve'
    
    fig = plt.figure()
    plt.plot(data[0], data[1], f'{line_types[0]}', c=colours[1])#, label=plot_label)
    #plt.xlim(axis_ranges[0][0], axis_ranges[0][1])
    #plt.ylim(axis_ranges[1][0], axis_ranges[1][1])
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    #plt.legend()
    plt.xlabel(axis_labels[0], fontsize=16)
    plt.ylabel(axis_labels[1], fontsize=16)
    plt.axhline(color='k')
    plt.axvline(color='k')
    plt.title(plot_title, fontsize=18)
    
    



if __name__ == '__main__':
    #plot_planform()
    plot_cl_cd_curve()
