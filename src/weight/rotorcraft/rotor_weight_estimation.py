import numpy as np
import matplotlib.pyplot as plt

class SingleRotorSizingEstimation:
    
    def __init__(self, MTOW, Range, number_of_rotor_blades):
        """
        params: 
            MTOW in kg
            range in m
            n_blades as an integer
        """
        self.MTOW = MTOW
        self.Range = Range
        self.n_blades = number_of_rotor_blades
        self.D_L = self.disk_loading()
        self.d = self.rotor_diameter()
        self.c = self.chord_length()
        self.Wf = self.fuel_weight()
        self.Wu = self.useful_weight()
        self.Wp = self.payload_weight()
        self.We = self.empty_weight()
        self.Vm = self.maximum_speed()

    def disk_loading(self):
        """
        Calculates the disk loading in kg/m^2
        """
        a4 = 2.28
        a5 = 2.34
        Dl = a4 * (self.MTOW**(1/3) - a5)
        return Dl
    
    def rotor_diameter(self):
        """
        Calculates the rotor diameter in m
        """
        d = 0.977 * self.MTOW**0.308
        return d
    
    def chord_length(self):
        """
        Calculates the chord length of the main rotor blade in m
        """
        c = 0.0108 * self.MTOW**0.539 / self.n_blades**0.714
        return c
    
    def blade_area(self):
        """
        Calculates the total blade area in m^2
        """
        blade_area = self.d/2 * self.c * self.n_blades
        return blade_area 

    def disk_area(self):
        """
        Calculates the disk area in m^2
        """
        disk_area = np.pi*(self.d/2)**2
        return disk_area
    
    def solidity(self):
        """
        Calculates the blade area over disk area ratio
        """
        return self.blade_area()/self.disk_area()  
    
    def fuel_weight(self):
        """
        Calculates the fuel weight in kg
        """
        Wf = 0.0038 * self.MTOW**0.976 * self.Range**0.650
        return Wf      
    
    def useful_weight(self):
        """
        Calculates the useful weight in kg
        Wu = Wp + Wf
        """
        Wu = 0.4709 * self.MTOW**0.99
        return Wu
    
    def payload_weight(self):
        """
        Calculates the payload weight in kg
        """
        Wp = self.Wu - self.Wf
        return Wp
    
    def empty_weight(self):
        """
        Calculates the empty weight in kg
        """
        OEW =  0.4854 * self.MTOW**1.015
        return OEW
    
    def maximum_takeoff_weight(self):
        """
        Calculates the maximum takeoff weight in kg
        """
        W0 = self.We + self.Wu
        return W0
    
    def maximum_speed(self):
        """
        Calculates the maximum speed at sea level in m/s
        """
        Vmax = (9.133 * self.MTOW**(0.380) / self.d)**(1/0.515)
        return Vmax
    
    def take_off_total_power(self):
        """
        Calculates the take-off total power in kW
        """
        P_TO = 0.0764 * self.MTOW**1.1455
        return P_TO
    
    def maximum_continuous_total_power(self):
        """
        Calculates the maximum continuous total power in kW
        """
        P_MC = 0.00126 * self.MTOW**0.9876 * self.Vm**0.9760
        return P_MC
    


class IntermeshingRotorSizingEstimation:
    """
    Note that the empty weight from the single rotor is multiplied by certain factor to convert it to 
    an intermeshing rotor.
    """
    
    def __init__(self, MTOW, Range, number_of_rotor_blades):
        self.single_rotor = SingleRotorSizingEstimation(MTOW, Range, number_of_rotor_blades)
        self.MTOW = MTOW
        self.Range = Range
        self.number_of_rotor_blades = number_of_rotor_blades
        self.Wf = self.single_rotor.fuel_weight()
        self.We = self.single_rotor.We * 1.9/2.5
        self.Wu = self.MTOW - self.We
        self.Wp = self.Wu - self.Wf
        
        
class CoaxialRotorSizingEstimation:
    """
    Note that the empty weight from the single rotor is multiplied by a certain factor to convert it to 
    an intermeshing rotor.
    """
    
    def __init__(self, MTOW, Range, number_of_rotor_blades):
        self.single_rotor = SingleRotorSizingEstimation(MTOW, Range, number_of_rotor_blades)
        self.MTOW = MTOW
        self.Range = Range
        self.number_of_rotor_blades = number_of_rotor_blades
        self.Wf = self.single_rotor.fuel_weight()
        self.We = self.single_rotor.We * 1.9/1.8
        self.Wu = self.MTOW - self.We
        self.Wp = self.Wu - self.Wf
        
    
        
   
    
if __name__ == '__main__':
    single = SingleRotorSizingEstimation(4000, 350, 4)
    inter = IntermeshingRotorSizingEstimation(4000, 350, 4)
    coaxial = CoaxialRotorSizingEstimation(4000, 350, 4)

    def plot_payload_range(MTOW, number_of_rotors):
        """
        Plots the payload vs range for the single, inter and coaxial configurations
        :param: Maximum Take-Off Weight in kg
        :param: number of rotors
        """
        range_list = np.arange(0,2000,20) # m
        single_payload_list, inter_payload_list, coaxial_payload_list = [], [], []
        
        for Range in range_list:
            single = SingleRotorSizingEstimation(MTOW, Range, number_of_rotors)
            inter = IntermeshingRotorSizingEstimation(MTOW, Range, number_of_rotors)
            coxial = CoaxialRotorSizingEstimation(MTOW, Range, number_of_rotors)
            
            single_payload_list.append(single.Wp)
            inter_payload_list.append(inter.Wp)
            coaxial_payload_list.append(coxial.Wp)
            
        plt.plot(range_list,single_payload_list, label='Single rotor')
        plt.plot(range_list,inter_payload_list, label='Intermeshing rotor')
        plt.plot(range_list,coaxial_payload_list, label='Coaxial rotor')
        plt.xlabel('Range (km)')
        plt.ylabel('Payload (kg)')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.vlines(x=0, ymin=0, ymax=2000)
        plt.grid()
        plt.legend()
        plt.show()
        
plot_payload_range(4000, 4)
