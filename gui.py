import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QGroupBox,
    QGridLayout,
    QComboBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from engine import Engine
from diffuser import InletConditions
from plot_engine import plot_engine_results


class EngineGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Turbojet Engine Analyzer")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Left panel: inputs and results
        left_panel = QVBoxLayout()

        # Input parameters group
        input_group = QGroupBox("Engine Parameters")
        input_layout = QGridLayout()

        self.inputs = {}
        params = [
            ("Ambient Pressure (Pa)", "p", "101325"),
            ("Ambient Temperature (K)", "T", "288"),
            ("Flight Speed (m/s)", "u", "250"),
            ("Pressure Ratio", "pr", "8.3"),
            ("Turbine Inlet Temp (K)", "T04", "1250"),
            ("Fuel Heating Value (J/kg)", "Qr", "43e6"),
            ("Diffuser Efficiency", "eta_d", "0.95"),
            ("Compressor Efficiency", "eta_c", "0.82"),
            ("Combustor Efficiency", "eta_b", "0.98"),
            ("Turbine Efficiency", "eta_t", "0.88"),
            ("Nozzle Efficiency", "eta_n", "0.97"),
            ("Air Mass Flow (kg/s)", "mdot", "20"),
        ]

        for i, (label, key, default) in enumerate(params):
            lbl = QLabel(label)
            edit = QLineEdit(default)
            input_layout.addWidget(lbl, i, 0)
            input_layout.addWidget(edit, i, 1)
            self.inputs[key] = edit

        # Afterburner Group
        afterburner_group = QGroupBox("Afterburner Settings") 
        afterburner_layout = QGridLayout()

        # Afterburner toggle
        self.afterburner_toggle = QPushButton("OFF")
        afterburner_layout.addWidget(QLabel("Afterburner Toggle"), 0, 0)
        afterburner_layout.addWidget(self.afterburner_toggle, 0, 1)

        self.afterburner_toggle.setCheckable(True)
        self.afterburner_toggle.toggled.connect(self.afterburner_toggled)

        afterburner_params = [
            ("Temperature (K)", "T06", "2000"),
            ("Efficiency", "eta_ab", "0.95"),
            ("Fuel Heating Value (J/kg)", "Qr_ab", "43e6")
        ]

        for i, (label, key, default) in enumerate(afterburner_params):
            lbl = QLabel(label)
            edit = QLineEdit(default)
            afterburner_layout.addWidget(lbl, i+1, 0)
            afterburner_layout.addWidget(edit, i+1, 1)
            self.inputs[key] = edit

        # Add input group 
        input_group.setLayout(input_layout)
        left_panel.addWidget(input_group)

        # Add afterburner group
        afterburner_group.setLayout(afterburner_layout)
        left_panel.addWidget(afterburner_group)

        # Plot settings drop down
        self.plot_type = QComboBox()
        self.plot_type.addItems(["TS Diagram", "Station Diagram"])
        left_panel.addWidget(self.plot_type)

        # Plot button
        self.calc_button = QPushButton("Plot")
        self.calc_button.clicked.connect(self.calculate)
        left_panel.addWidget(self.calc_button)

        self.results_list = []

        # Clear Button
        self.clear_button = QPushButton("Clear Plot")
        self.clear_button.clicked.connect(self.clear)
        left_panel.addWidget(self.clear_button)

        # Results display
        result_group = QGroupBox("Results")
        result_layout = QVBoxLayout()
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        result_layout.addWidget(self.result_text)
        result_group.setLayout(result_layout)
        left_panel.addWidget(result_group)

        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setMaximumWidth(400)
        layout.addWidget(left_widget)

        # Right panel: plots
        right_panel = QVBoxLayout()

        self.canvas = None
        self.plot_widget = QWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_widget.setLayout(self.plot_layout)
        right_panel.addWidget(self.plot_widget)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        layout.addWidget(right_widget)

    def clear(self):
        self.results_list = []

    def afterburner_toggled(self, checked):
        if checked:
            self.afterburner_toggle.setText("ON")
        else:
            self.afterburner_toggle.setText("OFF")

    def calculate(self):
        try:
            # Parse inputs
            p = float(self.inputs["p"].text())
            T = float(self.inputs["T"].text())
            u = float(self.inputs["u"].text())
            pr = float(self.inputs["pr"].text())
            T04 = float(self.inputs["T04"].text())
            Qr = float(self.inputs["Qr"].text())
            eta_d = float(self.inputs["eta_d"].text())
            eta_c = float(self.inputs["eta_c"].text())
            eta_b = float(self.inputs["eta_b"].text())
            eta_t = float(self.inputs["eta_t"].text())
            eta_n = float(self.inputs["eta_n"].text())
            mdot_air = float(self.inputs["mdot"].text())

            T06 = float(self.inputs["T06"].text())
            eta_ab = float(self.inputs["eta_ab"].text())
            Qr_ab = float(self.inputs["Qr_ab"].text())

            # Create engine and solve
            inlet = InletConditions(p=p, T=T, u=u)
            if self.afterburner_toggle.text() == "OFF":
                engine = Engine(
                    inlet_cond=inlet,
                    pr=pr,
                    T04=T04,
                    Qr=Qr,
                    eta_d=eta_d,
                    eta_c=eta_c,
                    eta_b=eta_b,
                    eta_t=eta_t,
                    eta_n=eta_n,
                    mdot_air=mdot_air,
                )
            else:
                engine = Engine(
                    inlet_cond=inlet,
                    pr=pr,
                    T04=T04,
                    Qr=Qr,
                    eta_d=eta_d,
                    eta_c=eta_c,
                    eta_b=eta_b,
                    eta_t=eta_t,
                    eta_n=eta_n,
                    mdot_air=mdot_air,
                    T06=T06,
                    eta_ab=eta_ab,
                    Qr_ab=Qr_ab,
                    afterburner_included=True
                )

            results = engine.solve()
            self.results_list.append(results)

            # Display results
            output = "=" * 50 + "\n"
            output += "TURBOJET ENGINE RESULTS\n"
            output += "=" * 50 + "\n\n"

            output += "Station Conditions:\n"
            output += f"  Station 02: P={results['T02'].P0 / 1000:.2f} kPa, T={results['T02'].T0:.2f} K\n"
            output += f"  Station 03: P={results['T03'].P0 / 1000:.2f} kPa, T={results['T03'].T0:.2f} K\n"
            output += f"  Station 04: P={results['T04'].P0 / 1000:.2f} kPa, T={results['T04'].T0:.2f} K\n"
            output += f"  Station 05: P={results['T05'].P0 / 1000:.2f} kPa, T={results['T05'].T0:.2f} K\n"
            output += (
                f"  Nozzle Exit: u={results['ue']:.2f} m/s, T={results['Te']:.2f} K\n\n"
            )

            output += "Performance:\n"
            output += f"  Fuel-Air Ratio: {results['f']:.6f}\n"
            output += f"  Fuel Flow Rate: {results['f'] * mdot_air:.4f} kg/s\n"
            output += f"  Thrust: {results['Thrust'] / 1000:.2f} kN\n"
            output += f"  TSFC: {results['TSFC'] * 1000:.4f} (mg/s)/N\n"
            output += f"  Specific Impulse: {results['Isp']:.2f} s\n"

            self.result_text.setText(output)

            # Update plots
            if self.canvas:
                self.plot_layout.removeWidget(self.canvas)
                self.canvas.deleteLater()

            fig = plot_engine_results(
                self.results_list, inlet, plot_type=self.plot_type.currentText()
            )
            self.canvas = FigureCanvas(fig)
            self.plot_layout.addWidget(self.canvas)

        except Exception as e:
            self.result_text.setText(f"Error: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = EngineGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
