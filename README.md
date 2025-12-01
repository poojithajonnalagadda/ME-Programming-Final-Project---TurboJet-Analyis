# Turbojet and Afterburner Analysis

This repository contains the code for a 1D turbojet analysis to find property changes over each component in order to find Thrust, Specific Impulse (Isp), Thrust Specific Fuel Consumption (TSFC), and Exit Velocity. This project will ultilize Object-Oriented Programming Structure to make each component modular to allow for analysis on an arbitrary number of nodes (e.g compressor nodes, turbine nodes). There is also a GUI Interface to allow for user inputs and plots are generated to provide for a better visual.

## Assumptions
- Adiabatic flow (not necessarily isentropic)  
- Steady, quasi-1-dimensional  
- Ideal gas  
- Calorically perfect (constant specific heats)

## Inlet/Diffuser

Given , R, Ta we can find the speed of sound as  
$$
a=\gammaRTa
$$

With the speed of sound defined, we can find the Mach No. of the incoming air into the inlet of the turbojet as  
$$
Ma =\frac{u}{a}
$$  
where u is the velocity of the incoming air into the turbojet.

We can find the stagnation temperature of the incoming air as  
$$
T01=Ta(1+\tfrac{\gamma-1}{2}Ma^2)
$$

Because our diffuser is assumed to be adiabatic, the stagnation temperature at the outlet of the diffuser/inlet of the compressor is  
$$
T02=T01
$$

Using isentropic relations, we can relate the temperature ratio through the diffuser to the pressure ratio through the diffuser as  
$$
\frac{P02}{Pa}=\left(\frac{T02s}{Ta}\right)^{\frac{\gamma}{\gamma-1}}
$$  
Where T02s is the stagnation temperature at the outlet of the diffuser if the diffuser were isentropic. The above implies that  
$$
P02=Pa\left(\frac{T02s}{Ta}\right)^{\frac{\gamma}{\gamma-1}}
$$

Given that the adiabatic efficiency of the diffuser, d, is  
$$
d=\frac{h02s-h_a}{h02-h_a}=\frac{c_p(T02s-Ta)}{c_p(T02-Ta)}=\frac{T02s-Ta}{T02-Ta}
$$

The above implies that  
$$
T02s=d(T02-Ta) + Ta
$$

Thus, the stagnation pressure at the outlet of the diffuser/inlet to the compressor is  
$$
P02=Pa\left(\frac{T02s}{Ta}\right)^{\frac{\gamma}{\gamma-1}}
$$  
where  
$$
T02s=d(T02-Ta) + Ta
$$

and the stagnation temperature at the outlet of the diffuser/inlet to the compressor is  
$$
T02=T01
$$  
where  
$$
T01=Ta(1+\tfrac{\gamma-1}{2}Ma^2)
$$

## Compressor

Given c, the pressure ratio across the compressor, we can find the stagnation pressure at the outlet of the compressor (P03) as  
$$
P03=cP02
$$

Given that the adiabatic efficiency of the compressor, c, is  
$$
c=\frac{h03s-h02}{h03-h02}=\frac{c_p(T03s-T02)}{c_p(T03-T02)}=\frac{T03s-T02}{T03-T02}
$$

The above implies that  
$$
T03=T02+\frac{1}{c}(T03s-T02)
$$

Using isentropic relations, we can relate the temperature ratio through the compressor to the pressure ratio through the compressor as  
$$
\frac{T03s}{T02}=\left(\frac{P03}{P02}\right)^{\frac{\gamma-1}{\gamma}}
$$  
Where T03s is the stagnation temperature at the outlet of the compressor if the compressor were isentropic. The above implies that  
$$
T03s=T02\left(\frac{P03}{P02}\right)^{\frac{\gamma-1}{\gamma}}
$$

Thus, the stagnation pressure at the outlet of the compressor is  
$$
P03=cP02
$$  
The stagnation temperature at the outlet of the compressor is  
$$
T03=T02+\frac{1}{c}(T03s-T02)
$$  
where  
$$
T03s=T02\left(\frac{P03}{P02}\right)^{\frac{\gamma-1}{\gamma}}
$$

## Combustor

Assuming isobaric combustion, which is typical of jet turbines,  
$$
P04=P03
$$

Given that the temperature at the outlet of the combustor/inlet to the turbine is a design parameter, then T04 is known and given.

Given that the adiabatic efficiency of the burner (combustor) is  
$$
b=\frac{m_{tot}(h04-h03)}{m_f Q_R}
$$  
TODO: one can show that the fuel-to-air mixture ratio can be solved as  
$$
f=\frac{T04-T03}{Q_R b c_p - T04}
$$

## Turbine

Assuming there are no transmission losses, we can use conservation of energy to say that the magnitude of work extracted by the turbine is equal to the magnitude of work consumed by the compressor. Thus,  
$$
m_{tot}(h04-h05)=m_a(h03-h02)
$$  
$$
m_a(1+f)c_p(T04-T05)=m_a c_p(T03-T02)
$$  
$$
(1+f)(T04-T05)=(T03-T02)
$$  
$$
T05=T04-\frac{T03-T02}{1+f}
$$

Given that the adiabatic efficiency of the turbine, t, is  
$$
t=\frac{h04-h05}{h04-h05s}=\frac{c_p(T04-T05)}{c_p(T04-T05s)}=\frac{T04-T05}{T04-T05s}
$$  
The above implies that  
$$
T05s=T04-\frac{1}{t}(T04-T05)
$$

Using isentropic relations, we can relate the temperature ratio across the turbine to the pressure ratio across the turbine as  
$$
\frac{P05}{P04}=\left(\frac{T05s}{T04}\right)^{\frac{\gamma}{\gamma-1}}
$$  
Thus,  
$$
P05=P04\left(\frac{T05s}{T04}\right)^{\frac{\gamma}{\gamma-1}}
$$

## Nozzle

Because our nozzle is assumed to be adiabatic, the stagnation temperature at the nozzle exit is  
$$
T_{0e}=T05
$$

We can relate the stagnation temperature at the exit to the exit velocity, \(u_e\), as  
$$
T_{0e}=T05=T_e + \frac{u_e^2}{2 c_p}
$$  
The above implies that  
$$
u_e=\sqrt{2c_p (T05-T_e)}
$$

Given that the adiabatic efficiency of the nozzle, n, is  
$$
n=\frac{h05-h_e}{h05-h_{es}}=\frac{T05-T_e}{T05-T_{es}}
$$  
The above implies that  
$$
T_e=T05 - n (T05-T_{es})
$$  
Using isentropic relations, we can relate the temperature ratio through the nozzle to the pressure ratio through the nozzle as  
$$
\frac{T_{es}}{T05}=\left(\frac{P_e}{P05}\right)^{\frac{\gamma-1}{\gamma}}
$$  
Assuming \(P_e = P_a\).

Thus, the exit velocity at the exit of the nozzle is given as  
$$
u_e=\sqrt{2c_p (T05-T_e)}
$$  
where  
$$
T_e=T05 - n(T05-T_{es})
$$  
and  
$$
T_{es}=T05\left(\frac{P_e}{P05}\right)^{\frac{\gamma-1}{\gamma}}
$$  

Thrust becomes  
$$
T = m_a(1+f)u_e - m_a u
$$

## Afterburner

Assuming isobaric combustion in the afterburner, just like we have in the combustor, which is typical of jet turbines,  
$$
P06=P05
$$

The max temperature of the afterburner is a given provided by the user, and it represents the maximum temperature the walls of the afterburner can withstand.  
$$
T06=T_{\text{max,ab}}
$$

It should be noted that the subscripts change with the addition of the afterburner, so the inlet of the nozzle is now denoted with subscript 06, and the exit of the nozzle is now 07.

Before the addition of the afterburner, the total mass flow rate used to be:  
$$
m_{tot}=m_a(1+f)
$$

However, now with the addition of the afterburner, the total fuel ratio becomes  
$$
f_t = f + f_{ab}
$$

Leaving the new total mass flow rate being  
$$
m_{tot,ab}=m_a(1+f_t)
$$

The energy conservation of the turbojet with the afterburner can be found with the following expression:

$$
m_a(1+f)c_pT05 + m_a f_{ab} Q_{R,ab} = m_a(1+f+f_{ab}) c_p T_{07}
$$

This can then be simplified to solve for the fuel-air ratio with the afterburner:

$$
f_{ab} = \frac{(1+f)c_p(T_{07}-T05)}{Q_{R,ab}} - \frac{c_p T_{07}}{Q_{R,ab}}
$$

The purpose of an afterburner is to provide additional thrust to the aircraft, which means that the relationship used to find thrust would change to the following:

$$
T = m_a(1+f+f_{ab})u_e - m_a u
$$

The pressure momentum term is neglected in the relationship found above because the assumption that the exit pressure equals the ambient pressure.

The calculations for TSFC would also change, where the original mf term found on the numerator would be changed to account for the fuel-air ratio in the afterburner:  
$$
\dot m_f = m_a (f + f_{ab})
$$

