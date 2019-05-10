import numpy as np

class SingleRotorSizingEstimation:
    
    def __init__(self, MTOW, n_blades):
        self.MTOW = MTOW
        self.n_blades = n_blades
        self.D_L = self.disk_loading()
        self.d = self.rotor_diameter()

    def disk_loading(self):
        """
        Calculates the disk loading in kg/m^2
        """
        a4 = 2.28
        a5 = 2.34
        Dl = a4*(self.MTOW**(1/3) - a5)
        return Dl
    
    def rotor_diameter(self):
        """
        Calculates the rotor diameter in m
        """
        d = 0.977 * self.MTOW**0.308
        return d
    
    def maximum_speed(self):
        """
        Calculates the maximum speed at sea level in m/s
        """
        Vmax = (9.133*self.MTOW**(0.380)/self.d)**1/0.515
        return Vmax
    
    def chord_length(self):
        c = 0.0108*self.MTOW**0.539/self.n_blades**0.714
        return c
   
    
if __name__ == '__main__':
    s = SingleRotorSizingEstimation(4000, 4)
    print(s.chord_length())