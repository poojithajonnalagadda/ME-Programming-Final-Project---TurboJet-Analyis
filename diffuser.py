from dataclasses import dataclass
from math import sqrt

from node import Node, ThermoState


@dataclass
class InletConditions:
    p: float = 101325.0  # [Pa]
    T: float = 300.0  # [K]
    u: float = 0.0  # [m/s]


class Diffuser(Node):
    def get_inlet_conditions(self) -> InletConditions:
        return self.inlet

    def get_outlet_conditions(self) -> ThermoState:
        # Unpack some variables for readability
        Pa = self.inlet.p
        Ta = self.inlet.T
        k = self.fluid.gamma
        R = self.fluid.R

        # Calculate inlet Mach No.
        a = sqrt(k * R * Ta)  # [m/s] - Speed of Sound
        Ma = self.inlet.u / a

        # Calculate real and isentropic outlet total temperature
        T02 = Ta * (1 + 0.5 * (k - 1) * Ma**2)
        T02s = self.eta * (T02 - Ta) + Ta

        # Calculate real outlet total pressure
        P02 = Pa * (T02s / Ta) ** (k / (k - 1))

        return ThermoState(P02, T02)


if __name__ == "__main__":
    inlet = Diffuser(InletConditions(u=100), eta=0.9)

    print(inlet.get_outlet_conditions())
    print(inlet.get_inlet_conditions())
