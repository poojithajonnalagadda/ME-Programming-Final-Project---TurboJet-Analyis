# Turbojet and Afterburner Analysis

This repository contains code for 1D turbojet analysis to calculate property changes across each component and determine:
- Thrust
- Specific Impulse (Isp)
- Thrust Specific Fuel Consumption (TSFC)
- Exit Velocity

The project utilizes an **Object-Oriented Programming (OOP) structure** to make each component modular, enabling analysis with an arbitrary number of nodes (e.g., compressor stages, turbine stages). A **GUI interface** is included for user inputs, and plots are generated for visualization.

## Assumptions
- Adiabatic flow (not necessarily isentropic)
- Steady, quasi-1-dimensional flow
- Ideal gas
- Calorically perfect gas (constant specific heats)

## Component Analysis

### Inlet/Diffuser
Given `γ`, `R`, and `Ta`, the speed of sound is:

\[
a = \sqrt{\gamma R T_a}
\]

The Mach number of incoming air:

\[
M_a = \frac{u}{a}
\]

where `u` is the freestream velocity.

Stagnation temperature at inlet:

\[
T_{01} = T_a \left(1 + \frac{\gamma - 1}{2} M_a^2\right)
\]

For an adiabatic diffuser:

\[
T_{02} = T_{01}
\]

Using isentropic relations:

\[
\frac{P_{02}}{P_a} = \left(\frac{T_{02s}}{T_a}\right)^{\frac{\gamma}{\gamma-1}}
\]

where `T_{02s}` is the stagnation temperature for an isentropic diffuser.

Diffuser efficiency `η_d`:

\[
\eta_d = \frac{h_{02s} - h_a}{h_{02} - h_a} = \frac{c_p(T_{02s} - T_a)}{c_p(T_{02} - T_a)} = \frac{T_{02s} - T_a}{T_{02} - T_a}
\]

Thus:

\[
T_{02s} = \eta_d(T_{02} - T_a) + T_a
\]

Finally:

\[
P_{02} = P_a \left(\frac{T_{02s}}{T_a}\right)^{\frac{\gamma}{\gamma-1}}
\]

### Compressor
Given compressor pressure ratio `π_c`:

\[
P_{03} = \pi_c P_{02}
\]

Compressor efficiency `η_c`:

\[
\eta_c = \frac{h_{03s} - h_{02}}{h_{03} - h_{02}} = \frac{T_{03s} - T_{02}}{T_{03} - T_{02}}
\]

Thus:

\[
T_{03} = T_{02} + \frac{1}{\eta_c}(T_{03s} - T_{02})
\]

Using isentropic relations:

\[
T_{03s} = T_{02} \left(\frac{P_{03}}{P_{02}}\right)^{\frac{\gamma-1}{\gamma}}
\]

### Combustor
Assuming isobaric combustion:

\[
P_{04} = P_{03}
\]

Outlet temperature `T_{04}` is a design parameter.

Burner efficiency `η_b`:

\[
\eta_b = \frac{\dot{m}_{total}(h_{04} - h_{03})}{\dot{m}_f Q_R}
\]

Fuel-air ratio `f`:

\[
f = \frac{T_{04} - T_{03}}{\frac{Q_R \eta_b}{c_p} - T_{04}}
\]

### Turbine
Assuming no transmission losses (work extracted by turbine = work consumed by compressor):

\[
\dot{m}_{total}(h_{04} - h_{05}) = \dot{m}_a(h_{03} - h_{02})
\]

\[
\dot{m}_a(1+f)c_p(T_{04} - T_{05}) = \dot{m}_a c_p(T_{03} - T_{02})
\]

\[
(1+f)(T_{04} - T_{05}) = (T_{03} - T_{02})
\]

\[
T_{05} = T_{04} - \frac{T_{03} - T_{02}}{1+f}
\]

Turbine efficiency `η_t`:

\[
\eta_t = \frac{h_{04} - h_{05}}{h_{04} - h_{05s}} = \frac{T_{04} - T_{05}}{T_{04} - T_{05s}}
\]

\[
T_{05s} = T_{04} - \frac{1}{\eta_t}(T_{04} - T_{05})
\]

Pressure ratio:

\[
\frac{P_{05}}{P_{04}} = \left(\frac{T_{05s}}{T_{04}}\right)^{\frac{\gamma}{\gamma-1}}
\]

### Nozzle
For an adiabatic nozzle:

\[
T_{0e} = T_{05}
\]

Exit velocity:

\[
u_e = \sqrt{2c_p(T_{05} - T_e)}
\]

Nozzle efficiency `η_n`:

\[
\eta_n = \frac{h_{05} - h_e}{h_{05} - h_{es}} = \frac{T_{05} - T_e}{T_{05} - T_{es}}
\]

\[
T_e = T_{05} - \eta_n(T_{05} - T_{es})
\]

Assuming `P_e = P_a`:

\[
T_{es} = T_{05} \left(\frac{P_e}{P_{05}}\right)^{\frac{\gamma-1}{\gamma}}
\]

### Thrust (without afterburner)
\[
T = \dot{m}_a(1+f)u_e - \dot{m}_a u
\]

## Afterburner Analysis
Assuming isobaric combustion:

\[
P_{06} = P_{05}
\]

Maximum afterburner temperature `T_{06}` is a user-provided design limit:

\[
T_{06} = T_{\text{max,ab}}
\]

**Note:** With afterburner, nozzle inlet becomes station 06 and exit becomes station 07.

Total fuel-air ratio:

\[
f_t = f + f_{ab}
\]

Total mass flow rate:

\[
\dot{m}_{total,ab} = \dot{m}_a(1 + f_t)
\]

Energy conservation:

\[
\dot{m}_a(1+f)c_p T_{05} + \dot{m}_a f_{ab} Q_{R,ab} = \dot{m}_a(1+f+f_{ab})c_p T_{07}
\]

Solving for afterburner fuel-air ratio:

\[
f_{ab} = \frac{(1+f)c_p(T_{07} - T_{05})}{Q_{R,ab} - c_p T_{07}}
\]

### Thrust (with afterburner)
\[
T = \dot{m}_a(1+f+f_{ab})u_e - \dot{m}_a u
\]

*(Pressure momentum term neglected assuming P_e = P_a)*

### TSFC (with afterburner)
\[
\dot{m}_f = \dot{m}_a (f + f_{ab})
\]

\[
TSFC = \frac{\dot{m}_f}{T}
\]

## Usage
1. Run the GUI interface
2. Input component parameters (efficiencies, pressure ratios, temperatures)
3. View calculated performance metrics
4. Analyze generated plots for component behavior

## Dependencies
- Python 3.x
- NumPy
- Matplotlib
- (Additional dependencies as required)
