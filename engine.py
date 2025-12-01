from diffuser import Diffuser, InletConditions
from compressor import Compressor
from combustor import Combustor
from turbine import Turbine
from nozzle import Nozzle
from afterburner import Afterburner
from node import ThermoState
import math

class Engine:
    def __init__ (self, inlet_cond, pr, T04, Qr, eta_d, eta_c, eta_b, eta_t, eta_n, mdot_air, Pa, **kwargs):
        self.mdot_air = mdot_air
        self.Pa = Pa
        self.afterburner_included = kwargs.get('afterburner_included', False)
        eta_ab = kwargs.get('eta_ab')
        self.diff = Diffuser(inlet_cond, eta = eta_d)
        self.comp = Compressor(self.diff, pressure_ratio = pr, eta=eta_c)
        self.comb = Combustor(self.comp, T04 = T04, Qr = Qr, eta_b = eta_b)
        self.turb = Turbine(self.comb, eta_t = eta_t, T03 = None, T02 = None, f = None)
        if self.afterburner_included:
            eta_ab = kwargs['eta_ab']
            Qr_ab = kwargs['Qr_ab']
            T06 = kwargs['T06']
            self.afterburn = Afterburner(self.turb, eta_ab = eta_ab, Qr_ab = Qr_ab, T06 = T06)
            self.nozz = Nozzle(eta_n = eta_n, fluid = self.afterburn.fluid)
        else:
            self.afterburn = None
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
        self.turb.T03 = stage03.T0
        self.turb.T02 = stage02.T0
        self.turb.f=f
        stage05 = self.turb.get_outlet_conditions()
        #Afterburner
        if self.afterburner_included and self.afterburn is not None:
            stage06 = self.afterburn.get_outlet_conditions()
            f_ab = self.afterburn.f_ab
            f_tot = self.afterburn.f_tot
            self.nozz.set_inlet(stage06)
            afterburner_station = stage06
        else:
            self.nozz.set_inlet(stage05)
            f_ab = 0.0
            f_tot = f
            afterburner_station = None
        #Nozzle
        ue , Te = self.nozz.get_outlet_conditions(self.Pa)

        #Turbojet Performance Characteristics
        mdot_f = f * self.mdot_air
        u0 = self.diff.inlet.u
        if self.afterburner_included and self.afterburn is not None:
            Thrust = self.mdot_air * (1 + f_tot) * ue - self.mdot_air * u0
            mdot_f = self.mdot_air * f_tot
        else: 
            Thrust = self.mdot_air * (1 + f) * ue - self.mdot_air * u0
            mdot_f = self.mdot_air * f
        TSFC = mdot_f / Thrust
        Isp = Thrust / (mdot_f * 9.81)
        result =  {
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
        if self.afterburner_included and self.afterburn is not None:
            result["T06"] = stage06
            result["f_ab"] = f_ab
            result["f_total"] = f_tot
        return result

#Testing block
if __name__ == "__main__":
    inlet_condtions = InletConditions(p=101325, T=300, u=100)

    engine = Engine(inlet_condtions, pr=6, T04=2800, Qr=45e6, eta_d=1.0, eta_c=1.0, eta_b=1.0, eta_t=1.0, eta_n=1.0, mdot_air=50, Pa=101325)

    solution = engine.solve()

    print(solution)
