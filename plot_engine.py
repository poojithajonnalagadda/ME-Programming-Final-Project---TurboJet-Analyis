import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
import numpy as np
from node import Fluid

def plot_engine_results(results, inlet_cond, plot_type):
    """
    Plot pressure and temperature at each station, plus T-S diagram
    """
    stations = ['Inlet', 'Station 02', 'Station 03', 'Station 04', 'Station 05', 'Exit']
    
    # Extract pressure and temperature data
    pressures = np.array([
        inlet_cond.p,
        results['T02'].P0,
        results['T03'].P0,
        results['T04'].P0,
        results['T05'].P0,
        inlet_cond.p
    ])
    
    temperatures = np.array([
        inlet_cond.T,
        results['T02'].T0,
        results['T03'].T0,
        results['T04'].T0,
        results['T05'].T0,
        results['Te']
    ])

    # Baseline entropy and properties of air
    s0 = PropsSI("S", "P", inlet_cond.p, "T", inlet_cond.T, "Air")
    air = Fluid(gamma=1.4, R=287)

    # Compute specific entropies at each station, assuming calorically perfect
    entropies = air.cp * np.log(temperatures / inlet_cond.T) - air.R * np.log(pressures / inlet_cond.p) + s0

    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    
    if plot_type == "P and T vs Station":
        # Plot 1: Pressure and Temperature vs Station
        x_pos = range(len(stations))
        
        ax_twin = ax.twinx()
        
        line1 = ax.plot(x_pos, pressures / 1000, 'o-', color='#2E86AB', linewidth=2, 
                        markersize=8, label='Pressure')
        ax.set_xlabel('Station', fontsize=11)
        ax.set_ylabel('Pressure (kPa)', color='#2E86AB', fontsize=11)
        ax.tick_params(axis='y', labelcolor='#2E86AB')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(stations, rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        
        line2 = ax_twin.plot(x_pos, temperatures, 's-', color='#E63946', linewidth=2,
                            markersize=8, label='Temperature')
        ax_twin.set_ylabel('Temperature (K)', color='#E63946', fontsize=11)
        ax_twin.tick_params(axis='y', labelcolor='#E63946')
        
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax.legend(lines, labels, loc='upper left')
        ax.set_title('Pressure and Temperature at Each Station', fontsize=12, pad=15)
        
    elif plot_type == "TS":
        # Plot 2: T-S Diagram
        valid_s = [s for s in entropies if s is not None]
        valid_T = [T for s, T in zip(entropies, temperatures) if s is not None]
        
        if len(valid_s) > 0:
            ax.plot(valid_s, valid_T, 'o--', color='#F77F00', linewidth=2, markersize=8)
            
            # Add station labels
            station_labels = ['0', '02', '03', '04', '05', 'e']
            for s, T, label in zip(valid_s, valid_T, station_labels):
                ax.annotate(label, (s, T), xytext=(5, 5), textcoords='offset points',
                            fontsize=9, bbox=dict(boxstyle='round,pad=0.3', 
                            facecolor='yellow', alpha=0.3))
            
            # Add isobar lines
            s_min, s_max = min(valid_s), max(valid_s)
            s_range = s_max - s_min
            s_plot = np.linspace(s_min - 0.1*s_range, s_max + 0.1*s_range, 100)
            
            # Draw isobars for key pressure levels
            pressure_levels = [inlet_cond.p, results["T03"].P0, results["T05"].P0]  # [Pa]

            delta_s = entropies - s0

            for p in pressure_levels:
                delta_s = s_plot - s0
                T_isobar = inlet_cond.T * np.exp((delta_s + air.R * np.log(p / inlet_cond.p)) / air.cp)
                
                if len(T_isobar) > 2:
                    ax.plot(s_plot, T_isobar, '--', color='gray', alpha=0.4, linewidth=0.8)
                    if len(T_isobar) > 0:
                        ax.text(s_plot[-1], T_isobar[-1], f'{p / 1000:0.0f} kPa', 
                                fontsize=7, color='gray', alpha=0.6)
            
            ax.set_xlabel('Specific Entropy (J/kg·K)', fontsize=11)
            ax.set_ylabel('Temperature (K)', fontsize=11)
            ax.set_title('Temperature-Entropy Diagram', fontsize=12, pad=15)
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    from engine import Engine
    from diffuser import InletConditions
    
    inlet = InletConditions(p=101325, T=288, u=250)
    engine = Engine(
        inlet_cond=inlet,
        pr=10.0,
        T04=1400,
        Qr=43e6,
        eta_d=1.0,
        eta_c=1.0,
        eta_b=0.95,
        eta_t=0.95,
        eta_n=0.95,
        mdot_air=50,
        Pa=101325
    )
    
    results = engine.solve()
    plot_engine_results(results, inlet)
    plt.show()
