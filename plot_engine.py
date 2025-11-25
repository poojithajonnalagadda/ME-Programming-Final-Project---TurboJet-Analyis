import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
import numpy as np

def plot_engine_results(results, inlet_cond):
    """
    Plot pressure and temperature at each station, plus T-S diagram
    """
    stations = ['Inlet', 'Station 02', 'Station 03', 'Station 04', 'Station 05', 'Exit']
    
    # Extract pressure and temperature data
    pressures = [
        inlet_cond.p / 1000,
        results['T02'].P0 / 1000,
        results['T03'].P0 / 1000,
        results['T04'].P0 / 1000,
        results['T05'].P0 / 1000,
        inlet_cond.p / 1000
    ]
    
    temperatures = [
        inlet_cond.T,
        results['T02'].T0,
        results['T03'].T0,
        results['T04'].T0,
        results['T05'].T0,
        results['Te']
    ]
    
    # Calculate entropy at each station using CoolProp
    entropies = []
    for P, T in zip([p * 1000 for p in pressures], temperatures):
        try:
            s = PropsSI('S', 'P', P, 'T', T, 'Air')
            entropies.append(s)
        except:
            entropies.append(None)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Pressure and Temperature vs Station
    x_pos = range(len(stations))
    
    ax1_twin = ax1.twinx()
    
    line1 = ax1.plot(x_pos, pressures, 'o-', color='#2E86AB', linewidth=2, 
                     markersize=8, label='Pressure')
    ax1.set_xlabel('Station', fontsize=11)
    ax1.set_ylabel('Pressure (kPa)', color='#2E86AB', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='#2E86AB')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(stations, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3)
    
    line2 = ax1_twin.plot(x_pos, temperatures, 's-', color='#E63946', linewidth=2,
                          markersize=8, label='Temperature')
    ax1_twin.set_ylabel('Temperature (K)', color='#E63946', fontsize=11)
    ax1_twin.tick_params(axis='y', labelcolor='#E63946')
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    ax1.set_title('Pressure and Temperature at Each Station', fontsize=12, pad=15)
    
    # Plot 2: T-S Diagram
    valid_s = [s for s in entropies if s is not None]
    valid_T = [T for s, T in zip(entropies, temperatures) if s is not None]
    
    if len(valid_s) > 0:
        ax2.plot(valid_s, valid_T, 'o-', color='#F77F00', linewidth=2, markersize=8)
        
        # Add station labels
        station_labels = ['0', '02', '03', '04', '05', 'e']
        for i, (s, T, label) in enumerate(zip(valid_s, valid_T, station_labels)):
            ax2.annotate(label, (s, T), xytext=(5, 5), textcoords='offset points',
                        fontsize=9, bbox=dict(boxstyle='round,pad=0.3', 
                        facecolor='yellow', alpha=0.3))
        
        # Add isobar lines
        s_min, s_max = min(valid_s), max(valid_s)
        s_range = s_max - s_min
        s_plot = np.linspace(s_min - 0.1*s_range, s_max + 0.1*s_range, 100)
        
        # Draw isobars for key pressure levels
        pressure_levels = [100, 200, 500, 1000, 1500]  # kPa
        for p_kpa in pressure_levels:
            T_isobar = []
            s_isobar = []
            for s_val in s_plot:
                try:
                    T_val = PropsSI('T', 'S', s_val, 'P', p_kpa * 1000, 'Air')
                    if 250 < T_val < 2000:
                        T_isobar.append(T_val)
                        s_isobar.append(s_val)
                except:
                    continue
            
            if len(T_isobar) > 2:
                ax2.plot(s_isobar, T_isobar, '--', color='gray', alpha=0.4, linewidth=0.8)
                if len(T_isobar) > 0:
                    ax2.text(s_isobar[-1], T_isobar[-1], f'{p_kpa}', 
                            fontsize=7, color='gray', alpha=0.6)
        
        ax2.set_xlabel('Specific Entropy (J/kg·K)', fontsize=11)
        ax2.set_ylabel('Temperature (K)', fontsize=11)
        ax2.set_title('Temperature-Entropy Diagram', fontsize=12, pad=15)
        ax2.grid(True, alpha=0.3)
    
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
        eta_d=0.95,
        eta_c=0.85,
        eta_b=0.98,
        eta_t=0.88,
        eta_n=0.95,
        mdot_air=50,
        Pa=101325
    )
    
    results = engine.solve()
    plot_engine_results(results, inlet)
    plt.show()
