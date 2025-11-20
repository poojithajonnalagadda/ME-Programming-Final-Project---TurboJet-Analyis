from node import ThermoState, Fluid
import math

class Nozzle:
    def __init__(self, eta_n: float = 1.0, fluid=Fluid(gamma = 1.4, R = 287)):
        self.inlet = None
        self.eta = eta_n
        self.fluid = fluid
        
    def set_inlet(self, inlet_state: ThermoState):
        self.inlet = inlet_state

    def get_outlet_conditions(self, Pa):
        P05 = self.inlet.P0
        T05 = self.inlet.T0
        k = self.fluid.gamma
        cp = self.fluid.cp
        
        # Isentropic exit static temperature
        Tes = T05 * (Pa / P05) ** ((k-1)/k)
        
        #Real Exit Temperature
        Te = T05 - self.eta * (T05 - Tes)
        
        #Exit Veolcity
        ue = math.sqrt(2 * cp * (T05 - Te))

        return ue, Te
