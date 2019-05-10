import numpy as np
import matplotlib.pyplot as plt

class SingleRotorSizingEstimation:
    
    def __init__(self, MTOW, range, n_blades):
        self.MTOW = MTOW
        self.range = range
        self.n_blades = n_blades
        self.D_L = self.disk_loading()
        self.d = self.rotor_diameter()
        self.c = self.chord_length()
        self.Wf = self.fuel_weight()
        self.Wu = self.useful_weight()
        self.We = self.empty_weight()

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
    
    def fuel_weight(self):
        """
        Calculates the fuel weight in kg
        """
        Wf = 0.0038 * self.MTOW**0.976 * self.range**0.650
        return Wf
    
    def solidity(self):
        """
        Calculates the blade area over disk area ratio
        """
        return self.blade_area()/self.disk_area()        
    
    def payload_weight(self):
        """
        Calculates the payload weight in kg
        """
        Wp = self.Wu - self.Wf
        return Wp
    
    def useful_weight(self):
        """
        Calculates the useful weight in kg
        Wu = Wp + Wf
        """
        Wu = 0.4709 * self.MTOW**0.99
        return Wu
    
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
        Vmax = (9.133 * self.MTOW**(0.380) / self.d)**1/0.515
        return Vmax
        
   
    
if __name__ == '__main__':
    s = SingleRotorSizingEstimation(4000, 350, 2)
    
    MTOW = 4000 #kg
    range_list = np.arange(0,2000,20)
    no_rotors = 4
    payload_list = []
    for range in range_list:
        s = SingleRotorSizingEstimation(MTOW, range, no_rotors)
        payload_list.append(s.payload_weight())
    plt.plot(range_list,payload_list)
    plt.show()
