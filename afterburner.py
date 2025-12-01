from node import Node, ThermoState
class Afterburner(Node):
    def __init__(self, inlet: Node, eta_ab: float = 1.0, Qr_ab:float = 1.0, T06:float = 1.0, afterburner: bool = True):
        super().__init__(inlet, eta_ab)
        self.T06 = T06
        self.Qr = Qr_ab
        self.f_ab = None
        self.f_tot = None
        self.included = afterburner
        
    def get_outlet_conditions(self):
        inlet = self.get_inlet_conditions()
        P05 = inlet.P0 #P05 = P06 b/c isobaric combustion
        T05 = inlet.T0
        cp = self.fluid.cp
        f = self.inlet.f
        
        #Afterburner fuel-air ratio
        self.f_ab = (1 + f) * cp * (self.T06 - T05) / ((self.Qr * self.eta) / cp - self.T06)
        self.f_tot = f + self.f_ab

        return ThermoState(P05, self.T06)
