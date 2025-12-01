from node import Node, ThermoState
class Turbine(Node):
    def __init__(self, inlet: Node, eta_t: float = 1.0, T03: float = None, T02: float = None, f: float = None):
        super().__init__(inlet, eta_t)
        self.T03 = T03
        self.T02 = T02
        self.f = f
        
    def get_outlet_conditions(self):
        # Unpack some variables for readability
        inlet = self.get_inlet_conditions()
        P04 = inlet.P0
        T04 = inlet.T0
        k = self.fluid.gamma

        # Turbine Outlet Temperaure (actual/non-isentropic)
        T05 = T04 - (self.T03 - self.T02) / (1 + self.f)
        
        #Isentropic (constant entropy) Temperature Drop
        T05s = T04 - (T04 - T05) / self.eta
        
        #Pressure drop across the turbine
        P05 = P04 * (T05s / T04) ** (k / (k - 1))

        return ThermoState(P05, T05)
