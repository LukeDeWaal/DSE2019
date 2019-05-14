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
        self.R = Range
        self.n_blades = number_of_rotor_blades
        self.D_L = self.disk_loading()
        self.d = self.rotor_diameter()
        self.c = self.chord_length()
        self.Wf = self.fuel_weight()
        self.Wp = self.payload_weight()
        self.Wu = self.useful_weight()
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
        Wf = 0.0038 * self.MTOW**0.976 * self.R**0.650
        return Wf      
    
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
    an intermeshing rotor. The ratio between the payload and fuel weight is 2:1 according to the single rotor
    estimation, so that ratio is used here as well, but this can be changed to our needs obviously.
    """
    
    def __init__(self, MTOW, Range, number_of_rotor_blades):
        self.single_rotor = SingleRotorSizingEstimation(MTOW, Range, number_of_rotor_blades)
        self.MTOW = MTOW
        self.Range = Range
        self.number_of_rotor_blades = number_of_rotor_blades
        self.We = self.single_rotor.MTOW/2.5
        self.Wu = self.MTOW - self.We
        self.Wp = self.Wu * 2/3
        self.Wf = self.Wu * 1/3
        
        
class CoaxialRotorSizingEstimation:
    """
    Note that the empty weight from the single rotor is multiplied by a certain factor to convert it to 
    an intermeshing rotor. The ratio between the payload and fuel weight is 2:1 according to the single rotor
    estimation, so that ratio is used here as well, but this can be changed to our needs obviously.
    """
    
    def __init__(self, MTOW, Range, number_of_rotor_blades):
        self.single_rotor = SingleRotorSizingEstimation(MTOW, Range, number_of_rotor_blades)
        self.MTOW = MTOW
        self.Range = Range
        self.number_of_rotor_blades = number_of_rotor_blades
        self.We = self.single_rotor.MTOW/1.8
        self.Wu = self.MTOW - self.We
        
    
        
   
    
if __name__ == '__main__':

    import unittest as ut

    single = SingleRotorSizingEstimation(4000, 350, 4)
    inter = IntermeshingRotorSizingEstimation(4000, 350, 4)
    coaxial = CoaxialRotorSizingEstimation(4000, 350, 4)


    class SizingEstimationTestCases(ut.TestCase):

        def setUp(self) -> None:

            self.MTOW = 4000
            self.Range = 350
            self.n_blades = 4

            self.single = SingleRotorSizingEstimation(self.MTOW, self.Range, self.n_blades)
            self.inter = IntermeshingRotorSizingEstimation(self.MTOW, self.Range, self.n_blades)
            self.coaxial = CoaxialRotorSizingEstimation(self.MTOW, self.Range, self.n_blades)

        def tearDown(self) -> None:
            pass

        def test_diskloading(self):

            self.assertNotEqual(self.single.disk_loading(), 0.0)
            # self.assertNotEqual(self.inter.disk_loading(), 0.0)   # Uncomment when implemented
            # self.assertNotEqual(self.coaxial.disk_loading(), 0.0) # Uncomment when implemented

            self.assertEqual(self.single.disk_loading(), 2.28*(self.MTOW**(1/3)-2.34))
            # self.assertEqual(self.single.disk_loading(), 2.28 * (self.MTOW ** (1 / 3) - 2.34)) # Uncomment when implemented
            # self.assertEqual(self.single.disk_loading(), 2.28 * (self.MTOW ** (1 / 3) - 2.34)) # Uncomment when implemented

        def test_rotor_diameter(self):
            pass

        def test_chordlength(self):
            pass

        def test_blade_area(self):
            pass

        def test_disk_area(self):
            pass

        def test_solidity(self):
            pass

        def test_fuel_weight(self):
            pass

        def test_payload_weight(self):
            pass

        def test_useful_weight(self):
            pass

        def test_empty_weight(self):
            pass

        def test_mtow(self):
            pass

        def test_max_speed(self):
            pass

        def test_takeoff_power(self):
            pass

        def test_max_continuous_power(self):
            pass

# =============================================================================
#     MTOW = 4000 #kg
#     range_list = np.arange(0,2000,20)
#     no_rotors = 4
#     payload_list = []
#     for range in range_list:
#         s = SingleRotorSizingEstimation(MTOW, range, no_rotors)
#         payload_list.append(s.payload_weight())
#     plt.plot(range_list,payload_list)
#     plt.xlabel('Range (km)')
#     plt.hlines(y=0, xmin=0, xmax=2000)
#     plt.vlines(x=0, ymin=0, ymax=2000)
#     plt.show()
# =============================================================================
