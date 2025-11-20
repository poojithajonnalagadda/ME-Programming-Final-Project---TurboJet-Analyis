import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QComboBox,
    QDial,
    QSlider,
    QLabel,
    QLineEdit,
)
from PyQt6.QtCore import Qt
from engine import Engine
from diffuser import InletConditions

class MainWindow(QMainWindow):
    class TurbojetGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Turbojet Analyzer")
        self.resize(900, 600) # IDK if these numbers are right I got them from the Py.QT Group lightning talk
        
    def main():
        
    if __name__ == "__main__":
        main()

