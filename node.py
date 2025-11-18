from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ThermoState:
    P0: float  # [Pa]
    T0: float  # [K]


@dataclass
class Fluid:
    gamma: float  # [1]
    R: float  # [J/(kg*K)]

    @property
    def cp(self) -> float:
        return self.gamma * self.R / (self.gamma - 1)  # [J/(kg*K)]


class Node(ABC):
    def __init__(self, inlet, eta: float = 1.0, fluid=Fluid(gamma=1.4, R=287)):
        self.inlet = inlet
        self.eta = eta
        self.fluid = fluid

    def get_inlet_conditions(self) -> ThermoState:
        return self.inlet.get_outlet_conditions()

    @abstractmethod
    def get_outlet_conditions(self) -> ThermoState:
        pass
