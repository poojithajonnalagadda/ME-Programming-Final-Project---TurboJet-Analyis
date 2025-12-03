from node import ThermoState, Fluid
import math


class Nozzle:
    def __init__(self, eta_n: float = 1.0, fluid=Fluid(gamma=1.4, R=287)):
        self.inlet = None
        self.eta = eta_n
        self.fluid = fluid

    def set_inlet(self, inlet_state: ThermoState):
        self.inlet = inlet_state

    def get_outlet_conditions(self, Pa):
        P0_inlet = self.inlet.P0
        T0_inlet = self.inlet.T0
        k = self.fluid.gamma
        cp = self.fluid.cp

        # Isentropic exit static temperature
        Tes = T0_inlet * (Pa / P0_inlet) ** ((k - 1) / k)

        # Real Exit Temperature
        Te = T0_inlet - self.eta * (T0_inlet - Tes)

        # Exit Veolcity
        ue = math.sqrt(2 * cp * (T0_inlet - Te))

        return ue, Te
