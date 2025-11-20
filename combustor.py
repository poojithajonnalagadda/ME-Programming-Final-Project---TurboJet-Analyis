from node import Node, ThermoState

class Combustor(Node): 
    def __init__(self, inlet: Node, eta_b: float = 1.0, Qr:float = 1.0, T04:float = 1.0):
        super().__init__(inlet, eta_b)
        self.T04 = T04 #Turbine Inlet Temp Given
        self.Qr = Qr
        self.f = None

    def get_outlet_conditions(self):
        inlet = self.get_inlet_conditions()
        P03 = inlet.P0 #P02 = P03
        T03 = inlet.T0 
        cp = self.fluid.cp
        #Fuel-air ratio
        self.f = (self.T04 - T03) / ((self.Qr * self.eta) / cp - self.T04)
        
        return ThermoState(P03, self.T04)
