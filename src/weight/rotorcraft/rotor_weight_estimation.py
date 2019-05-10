class SingleRotorSizingEstimation:
    
    def __init__(self, MTOW, range, n_blades):
        self.MTOW = MTOW
        self.range = range
        self.n_blades = n_blades
        self.D_L = self.disk_loading()
        self.d = self.rotor_diameter()
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
    
    def maximum_speed(self):
        """
        Calculates the maximum speed at sea level in m/s
        """
        Vmax = (9.133 * self.MTOW**(0.380) / self.d)**1/0.515
        return Vmax
    
    def chord_length(self):
        """
        Calculates the chord length of the main rotor blade in m
        """
        c = 0.0108 * self.MTOW**0.539 / self.n_blades**0.714
        return c
    
    def fuel_weight(self):
        """
        Calculates the fuel weight in kg
        """
        Wf = 0.0038 * self.MTOW**0.976 * self.range**0.650
        return Wf
        
    
    def payload_weight(self):
        """
        Calculates the payload weight in kg
        """
        Wp = self.Wf - self.Wu
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
        
   
    
if __name__ == '__main__':
    s = SingleRotorSizingEstimation(4000, 350, 4)
    for i in range(0,100):
        s = SingleRotorSizingEstimation(s.maximum_takeoff_weight(), 350, 4)
        print(s.maximum_takeoff_weight())