from PyQt6 import QtWidgets, QtCore


def increment(grbl_instance, move_code):
    grbl_instance.write('G91') # Use absolute positioning
    grbl_instance.write(f'G1 {move_code}')
    grbl_instance.job_run()


class RobotWindow(QtWidgets.QMainWindow):
    item_created = QtCore.pyqtSignal(str)

    def __init__(self, grbl_instance):
        super().__init__()
        self.setWindowTitle("Control Robot")

        self.py_button = QtWidgets.QPushButton("+Y", self)
        self.py_button.clicked.connect(lambda: increment(grbl_instance, 'Y1')) # Move 1 mm
        self.pz_button = QtWidgets.QPushButton("+Z", self)
        self.pz_button.clicked.connect(lambda: increment(grbl_instance, 'Z1'))
        self.nx_button = QtWidgets.QPushButton("-X", self)
        self.nx_button.clicked.connect(lambda: increment(grbl_instance, 'X-1'))
        self.ny_button = QtWidgets.QPushButton("-Y", self)
        self.ny_button.clicked.connect(lambda: increment(grbl_instance, 'Y-1'))
        self.px_button = QtWidgets.QPushButton("+X", self)
        self.px_button.clicked.connect(lambda: increment(grbl_instance, 'X1'))
        self.nz_button = QtWidgets.QPushButton("-Z", self)
        self.nz_button.clicked.connect(lambda: increment(grbl_instance, 'Z-1'))

        robot_controls = QtWidgets.QWidget()
        robot_controls_layout = QtWidgets.QGridLayout(robot_controls)

        robot_controls_layout.addWidget(self.py_button, 0, 1)
        robot_controls_layout.addWidget(self.pz_button, 0, 3)
        robot_controls_layout.addWidget(self.nx_button, 1, 0)
        robot_controls_layout.addWidget(self.ny_button, 1, 1)
        robot_controls_layout.addWidget(self.px_button, 1, 2)
        robot_controls_layout.addWidget(self.nz_button, 1, 3)

        self.setCentralWidget(robot_controls)
