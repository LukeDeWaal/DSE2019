import matplotlib.pyplot as plt
import pandas as pd
from parameters import *



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
    # top view
    plt.subplot(2,1,1)
    
    # CG
    plt.plot(0, -cg_position, marker='o', markersize=3, color='red', label='Center of Gravity') 
     
    # center of gravity
    plt.plot(0, -wing_position, marker='o', markersize=3, color='blue', label='Center of Pressure') 
        
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
    Plots the Cl-alpha curve, of the NACA 6420, based on JavaFoil
    """
    plt.plot(list(range(0,21,1)), 
             [0.706, 0.796, 0.898, 0.997, 1.093, 1.188, 1.279, 1.368, 1.454, 1.534, 1.608, 1.675, 1.733, 1.780, 1.814, 1.837, 1.844, 1.838, 1.818, 1.786, 1.739])
    plt.plot([0,10], [0.706, 1.6])
    plt.xlabel('alpha')
    plt.ylabel('Cl')
    plt.grid()
    plt.show()
    
    
def plot_naca_6415():
    coordinates = pd.read_fwf('NACA_6415_coordinates.txt', names=['x', 'y'])
    plt.plot(coordinates['x'], coordinates['y'])
    plt.axis('equal')
    plt.grid()
    plt.show()



if __name__ == '__main__':
    plot_planform()