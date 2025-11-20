from node import Node, ThermoState
class Turbine(Node):
    def __init__(self, inlet: Node, eta_t: float = 1.0):
        super().__init__(inlet, eta_t)

    def get_outlet_conditions(self, T03, T02, f):
        # Unpack some variables for readability
        inlet = self.get_inlet_conditions()
        P04 = inlet.P0
        T04 = inlet.T0
        k = self.fluid.gamma

        # Turbine Outlet Temperaure (actual/non-isentropic)
        T05 = T04 - (T03 - T02) / (1 + f)
        
        #Isentropic (constant entropy) Temperature Drop
        T05s = T04 - (T04 - T05) / self.eta
        
        #Pressure drop across the turbine
        P05 = P04 * (T05s / T04) ** (k / (k - 1))

        return ThermoState(P05, T05)
