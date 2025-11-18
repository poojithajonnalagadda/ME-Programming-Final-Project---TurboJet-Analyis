from diffuser import Diffuser, InletConditions
from compressor import Compressor


# Testing block
if __name__ == "__main__":
    inlet = InletConditions(p=100000, u=0)
    diffuser = Diffuser(inlet)
    compressor1 = Compressor(diffuser, pressure_ratio=3, eta=1.0)
    compressor2 = Compressor(compressor1, pressure_ratio=2, eta=1.0)

    print(inlet)
    print(diffuser.get_outlet_conditions())
    print(compressor1.get_outlet_conditions())
    print(compressor2.get_outlet_conditions())
