from diffuser import Diffuser, InletConditions
from compressor import Compressor
from combustor import Combustor
from turbine import Turbine
from nozzle import Nozzle
from node import ThermoState
import math

class Engine:
    def __init__ (self, inlet_cond, pr, T04, Qr, eta_d, eta_c, eta_b, eta_t, eta_n, mdot_air, Pa):
        self.mdot_air = mdot_air
        self.Pa = Pa
        self.diff = Diffuser(inlet_cond, eta = eta_d)
        self.comp = Compressor(self.diff, pressure_ratio = pr, eta=eta_c)
        self.comb = Combustor(self.comp, T04 = T04, Qr = Qr, eta_b = eta_b)
        self.turb = Turbine(self.comb, eta_t = eta_t)
        self.nozz = Nozzle(eta_n = eta_n, fluid = self.turb.fluid)
        
    def solve(self):
        #Diffuser
        stage02 = self.diff.get_outlet_conditions()
        #Compressor
        stage03 = self.comp.get_outlet_conditions()
        #Combustor
        stage04 = self.comb.get_outlet_conditions()
        f = self.comb.f
        #Turbine
        #stage05 = self.turb.get_outlet_conditions(T03 = stage03.T0, T02 = stage02.T0, f=f)
        stage05 = self.turb.get_outlet_conditions(T03 = stage03.T0, T02 = stage02.T0, f=f)
        #Nozzle
        self.nozz.set_inlet(stage05)
        ue , Te = self.nozz.get_outlet_conditions(self.Pa)

        #Turbojet Performance Characteristics
        mdot_f = f * self.mdot_air
        u0 = self.diff.inlet.u
        Thrust = self.mdot_air * (1 + f) * ue - self.mdot_air * u0
        TSFC = mdot_f / Thrust
        Isp = Thrust / (mdot_f * 9.81)
     # return all the stations as gui outputs somehow
        return{
        "T02": stage02,
        "T03": stage03,
        "T04": stage04,
        "T05": stage05,
        "ue": ue,
        "Te": Te,
        "f": f,
        "Thrust": Thrust,
        "TSFC": TSFC,
        "Isp": Isp
        }

#Testing block
if __name__ == "__main__":
    inlet = InletConditions(p=100000, u=0)
    diffuser = Diffuser(inlet)
    compressor1 = Compressor(diffuser, pressure_ratio=3, eta=1.0)
    compressor2 = Compressor(compressor1, pressure_ratio=2, eta=1.0)

    print(inlet)
    print(diffuser.get_outlet_conditions())
    print(compressor1.get_outlet_conditions())
    print(compressor2.get_outlet_conditions())
