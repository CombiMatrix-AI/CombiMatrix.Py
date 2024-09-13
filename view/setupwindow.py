import os
from PyQt6 import QtWidgets, QtCore

from view.gridwidget import GridWidget


class SetupWindow(QtWidgets.QMainWindow):
    item_created = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup Window")
        self.tab_widget = QtWidgets.QTabWidget(self)

        ##############################################################################################

        create_block_tab = QtWidgets.QWidget()
        create_block_layout = QtWidgets.QHBoxLayout(create_block_tab)

        create_block_button_sublayout = QtWidgets.QVBoxLayout()
        self.block_name_input = QtWidgets.QLineEdit(self)
        self.block_name_input.setPlaceholderText("Enter Block Name")
        create_block_button_sublayout.addWidget(self.block_name_input, 0,
                                                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.create_block_button = QtWidgets.QPushButton("Create Block")
        self.create_block_button.clicked.connect(self.create_block)
        create_block_button_sublayout.addWidget(self.create_block_button, 0,
                                                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.clear_grid_button = QtWidgets.QPushButton("Clear Grid")
        self.clear_grid_button.clicked.connect(lambda: self.grid_widget.clear())
        create_block_button_sublayout.addWidget(self.clear_grid_button, 0,
                                                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        spacer = QtWidgets.QSpacerItem(200, 300, QtWidgets.QSizePolicy.Policy.Fixed,
                                       QtWidgets.QSizePolicy.Policy.Minimum)
        create_block_button_sublayout.addItem(spacer)

        create_block_layout.addLayout(create_block_button_sublayout, 0)

        self.block_chipmap = [[0] * 16 for _ in range(64)]
        self.grid_widget = GridWidget(8, self.block_chipmap)
        create_block_layout.addWidget(self.grid_widget, 0,
                                      QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        ##############################################################################################

        create_cv_config_tab = QtWidgets.QWidget()
        create_cv_config_layout = QtWidgets.QGridLayout(create_cv_config_tab)

        self.create_cv_button = QtWidgets.QPushButton("Create CV Config")
        self.create_cv_button.clicked.connect(self.create_cv)
        create_cv_config_layout.addWidget(self.create_cv_button, 0, 0)

        self.cv_name_input = QtWidgets.QLineEdit(self)
        self.cv_name_input.setPlaceholderText("Enter CV Config Name")
        create_cv_config_layout.addWidget(self.cv_name_input, 0, 1)

        v_start_label = QtWidgets.QLabel("v_start")
        self.v_start_input = QtWidgets.QLineEdit(self)
        self.v_start_input.setText("0.5")

        v_end_label = QtWidgets.QLabel("v_end")
        self.v_end_input = QtWidgets.QLineEdit(self)
        self.v_end_input.setText("1.3")

        v_2_label = QtWidgets.QLabel("v_2")
        self.v_2_input = QtWidgets.QLineEdit(self)
        self.v_2_input.setText("0.2")

        v_final_label = QtWidgets.QLabel("v_final")
        self.v_final_input = QtWidgets.QLineEdit(self)
        self.v_final_input.setText("1.0")

        rate_label = QtWidgets.QLabel("rate")
        self.rate_input = QtWidgets.QLineEdit(self)
        self.rate_input.setText("0.05")

        step_label = QtWidgets.QLabel("step")
        self.step_input = QtWidgets.QLineEdit(self)
        self.step_input.setText("0.001")

        n_cycles_label = QtWidgets.QLabel("n_cycles")
        self.n_cycles_input = QtWidgets.QLineEdit(self)
        self.n_cycles_input.setText("2")

        begin_i_label = QtWidgets.QLabel("begin_i")
        self.begin_i_input = QtWidgets.QLineEdit(self)
        self.begin_i_input.setText("0.5")

        end_i_label = QtWidgets.QLabel("end_i")
        self.end_i_input = QtWidgets.QLineEdit(self)
        self.end_i_input.setText("1.0")

        # Add widgets to the create_cv_config_layout
        create_cv_config_layout.addWidget(v_start_label, 1, 0)
        create_cv_config_layout.addWidget(self.v_start_input, 1, 1)
        create_cv_config_layout.addWidget(v_end_label, 1, 2)
        create_cv_config_layout.addWidget(self.v_end_input, 1, 3)
        create_cv_config_layout.addWidget(v_2_label, 1, 4)
        create_cv_config_layout.addWidget(self.v_2_input, 1, 5)
        create_cv_config_layout.addWidget(v_final_label, 1, 6)
        create_cv_config_layout.addWidget(self.v_final_input, 1, 7)

        create_cv_config_layout.addWidget(rate_label, 2, 0)
        create_cv_config_layout.addWidget(self.rate_input, 2, 1)

        create_cv_config_layout.addWidget(step_label, 3, 0)
        create_cv_config_layout.addWidget(self.step_input, 3, 1)

        create_cv_config_layout.addWidget(n_cycles_label, 4, 0)
        create_cv_config_layout.addWidget(self.n_cycles_input, 4, 1)

        create_cv_config_layout.addWidget(begin_i_label, 5, 0)
        create_cv_config_layout.addWidget(self.begin_i_input, 5, 1)

        create_cv_config_layout.addWidget(end_i_label, 6, 0)
        create_cv_config_layout.addWidget(self.end_i_input, 6, 1)

        ##############################################################################################

        self.tab_widget.addTab(create_block_tab, "Create Block")
        self.tab_widget.addTab(create_cv_config_tab, "Create CV Config")
        self.setCentralWidget(self.tab_widget)

    def create_block(self):  # TODO: MOVE LOGIC TO BLOCKS FOLDER?
        first_row, first_col = -1, -1
        last_row, last_col = -1, -1

        for row in range(len(self.block_chipmap)):
            for col in range(len(self.block_chipmap[0])):
                if self.block_chipmap[row][col] != 0:
                    if first_row == -1 or row < first_row:
                        first_row = row
                    if first_col == -1 or col < first_col:
                        first_col = col
                    if row > last_row:
                        last_row = row
                    if col > last_col:
                        last_col = col

        width = last_row - first_row + 1 if first_row != -1 else 0
        length = last_col - first_col + 1 if first_col != -1 else 0

        block_definition = [col[first_col:last_col+1] for col in self.block_chipmap[first_row:last_row+1]]

        block_name = self.block_name_input.text()

        # Create the content for the .block file
        block_file_content = (
            "[Block Config]\n"
            f"Number Rows = {width}\n"
            f"Number Columns = {length}\n"
            f"Start Row = {first_row}\n"
            f"Start Column = {first_col}\n"
            f'Definition = {block_definition}\n'
        )

        # Ensure the blocks directory exists
        blocks_dir = os.path.join(os.path.dirname(__file__), '..', 'blocks')

        # Write the content to a .block file in the blocks folder
        with open(os.path.join(blocks_dir, f"{block_name}.block"), "w") as block_file:
            block_file.write(block_file_content)

        self.grid_widget.clear()
        self.item_created.emit(f"Block Created, {block_name}")

    def create_cv(self):
        start = float(self.v_start_input.text())
        end = float(self.v_end_input.text())
        E2 = float(self.v_2_input.text())
        Ef = float(self.v_final_input.text())
        rate = float(self.rate_input.text())
        step = float(self.step_input.text())
        N_cycles = int(self.n_cycles_input.text())
        begin_measuring_I = float(self.begin_i_input.text())
        End_measuring_I = float(self.end_i_input.text())

        cv_config_content = (
            "[Cyclic Voltammetry Config]\n"
            f"v_start = {start}\n"
            f"v_end = {end}\n"
            f"v_2 = {E2}\n"
            f"v_final = {Ef}\n"
            f"scan rate (V/s) = {rate}\n"
            f"voltage step = {step}\n"
            f"cycles = {N_cycles}\n"
            f"begin_measuring_I = {begin_measuring_I}\n"
            f"End_measuring_I = {End_measuring_I}\n"
        )

        cv_name = self.cv_name_input.text()  # Assuming you want to generate a common name or you can provide input for this

        # Ensure the cv_configs directory exists
        cv_configs_dir = os.path.join(os.path.dirname(__file__), '..', 'vcfgs', 'cv')

        # Write the content to a .cv.vcfg file in the cv_configs folder
        with open(os.path.join(cv_configs_dir, f"{cv_name}.cv.vcfg"), "w") as cv_file:
            cv_file.write(cv_config_content)

        self.item_created.emit(f"CV Config Created, {cv_name}")
