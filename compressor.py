from node import Node, ThermoState


class Compressor(Node):
    def __init__(self, inlet: Node, pressure_ratio: float, eta: float = 1.0):
        super().__init__(inlet, eta)
        self.pi = pressure_ratio

    def get_outlet_conditions(self) -> ThermoState:
        # Unpack some variables for readability
        inlet = self.get_inlet_conditions()
        P02 = inlet.P0
        T02 = inlet.T0
        k = self.fluid.gamma

        # Calculate real outlet total pressure
        P03 = self.pi * P02

        # Calculate real and isentropic outlet total temperature
        T03s = T02 * self.pi ** ((k - 1) / k)
        T03 = T02 + (T03s - T02) / self.eta

        return ThermoState(P03, T03)
