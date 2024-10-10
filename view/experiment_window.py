import platform
import os
import random
from PyQt6 import QtCore
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QWidget, QDialog, QMainWindow, \
    QApplication, QComboBox, QListWidget, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QDialogButtonBox, \
    QMessageBox
from grbl_streamer import GrblStreamer
import time

import experiment
import fileio
from definitions import ROOT_DIR, CONFIG, GET_ROBOT_ENABLED, GET_PAR_ENABLED, GET_COUNTER_ELECTRODE, \
    GET_REFERENCE_ELECTRODE, GET_WORKING_ELECTRODE
from view.create_block import CreateBlockWindow
from view.create_vcfg import CreateVcfgWindow

if platform.system() != 'Darwin':
    from par import PAR
    from adlink import Adlink
from view.grid_widget import GridWidget
from view.robot_window import RobotWindow

def grbl_callback(eventstring, *data):
    args = []
    for d in data:
        args.append(str(d))
    print("GRBL CALLBACK: event={} data={}".format(eventstring.ljust(30), ", ".join(args)))

def init_adlink():
    adlink_card = Adlink()
    print("DEBUG MESSAGE: Adlink Card Initialized")
    return adlink_card

def init_par():
    kbio_port = CONFIG.get('Ports', 'par_port')
    par = PAR(kbio_port)
    print("DEBUG MESSAGE: EC-Lab PAR Initialized")
    return par

def init_robot():
    grbl = GrblStreamer(grbl_callback)
    grbl.setup_logging()
    grbl_port = CONFIG.get('Ports', 'robot_port')
    grbl.cnect(grbl_port, 115200)
    print("DEBUG MESSAGE: GRBL Connected")
    time.sleep(1)  # Let grbl connect
    grbl.killalarm()  # Turn off alarm on startup
    print("DEBUG MESSAGE: GRBL Alarm Turned off")
    return grbl


class SolutionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Enter Solution Details")

        # Create input fields
        self.cas_input = QLineEdit(self)
        self.stock_input = QLineEdit(self)
        self.amount_input = QLineEdit(self)
        self.concentration_input = QLineEdit(self)

        # Set layout
        layout = QFormLayout()
        layout.addRow(QLabel("CAS #:", self), self.cas_input)
        layout.addRow(QLabel("Stock #:", self), self.stock_input)
        layout.addRow(QLabel("Amount (mL):", self), self.amount_input)
        layout.addRow(QLabel("Concentration (M):", self), self.concentration_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        self.setLayout(layout)

    def get_data(self):
        return {
            'cas': self.cas_input.text(),
            'stock': self.stock_input.text(),
            'amount': self.amount_input.text(),
            'concentration': self.concentration_input.text()
        }


class ExperimentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CombiMatrixAI")

        self.enable_robot = GET_ROBOT_ENABLED()
        self.enable_par = GET_PAR_ENABLED()
        self.enable_adlink = any(electrode.startswith("Chip: CBMX") for electrode in
                            [GET_COUNTER_ELECTRODE(), GET_WORKING_ELECTRODE(), GET_REFERENCE_ELECTRODE()])

        if not (self.enable_robot or self.enable_par or self.enable_adlink):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setText("Nothing is currently being controlled!"
                            "\n\n"
                            "Please enable either the robot, the PAR, or use a CMBX chip")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.buttonClicked.connect(QApplication.instance().quit)
            msg_box.exec()

        create_block_button = QPushButton("Create Block", self)
        chip_test_button = QPushButton("Run Chip Test", self)
        blocks_label = QLabel("Load Block:", self)
        self.blocks_dropdown = QComboBox(self)
        tile_block_button = QPushButton("Tile Block", self)
        self.blocks = {}
        if self.enable_adlink:
            if platform.system() != 'Darwin':
                self.adlink_card = init_adlink()

            self.blocks_dir = os.path.join(ROOT_DIR, 'blocks')
            self.blocks = fileio.from_folder(self.blocks_dir, '.block')

            self.create_block_window = CreateBlockWindow()
            self.create_block_window.item_created.connect(self.item_created)

            create_block_button.clicked.connect(self.create_block_window.show)
            chip_test_button.clicked.connect(lambda: self.chip_test(1))

            self.blocks_dropdown.addItems(list(self.blocks.keys()))

            tile_block_button.clicked.connect(lambda: self.tile_block())

            self.grid_widget = GridWidget(5)
        else:
            create_block_button.setEnabled(False)
            chip_test_button.setEnabled(False)
            blocks_label.setEnabled(False)
            self.blocks_dropdown.setEnabled(False)
            tile_block_button.setEnabled(False)

        create_vcfg_button = QPushButton("Create VCFG", self)
        vcfgs_label = QLabel("Load VCFG Config:", self)
        self.vcfgs_dropdown = QComboBox(self)
        self.vcfgs = {}
        if self.enable_par:
            if platform.system() != 'Darwin':
                self.par = init_par()

            self.create_vcfg_window = CreateVcfgWindow()
            self.create_vcfg_window.item_created.connect(self.item_created)

            create_vcfg_button.clicked.connect(self.create_vcfg_window.show)

            self.vcfg_dir = os.path.join(ROOT_DIR, 'vcfgs')
            self.vcfgs = fileio.from_folder(self.vcfg_dir, '.vcfg')

            self.vcfgs_dropdown.addItems(list(self.vcfgs.keys()))
        else:
            vcfgs_label.setEnabled(False)
            self.vcfgs_dropdown.setEnabled(False)

        robot_controls_button = QPushButton("Robot Controls", self)
        gcode_label = QLabel("Load G-code:", self)
        self.gcode_dropdown = QComboBox(self)
        execute_gcode_button = QPushButton("Execute G-code", self)
        self.gcode = {}
        if self.enable_robot:
            self.grbl = init_robot()

            self.gcode_dir = os.path.join(ROOT_DIR, 'gcode')
            self.gcode = fileio.from_folder(self.gcode_dir, '.gcode')

            self.robot_window = RobotWindow(self.grbl)
            robot_controls_button.clicked.connect(self.robot_window.show)

            self.gcode_dropdown.addItems(list(self.gcode.keys()))

            execute_gcode_button.clicked.connect(
                lambda: self.execute_gcode(self.experiments_list[self.curr_exp_index].gcode))
        else:
            robot_controls_button.setEnabled(False)
            gcode_label.setEnabled(False)
            self.gcode_dropdown.setEnabled(False)
            execute_gcode_button.setEnabled(False)


        run_cv_button = QPushButton("Run Experiments", self)
        run_cv_button.clicked.connect(self.run_experiments)
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(QApplication.instance().quit)

        solution_button = QPushButton("Enter Solution", self)
        solution_button.clicked.connect(self.enter_solution)
        self.solution_input = QLineEdit(self)
        self.solution_input.setReadOnly(True)

        save_experiment_button = QPushButton("New Experiment", self)
        save_experiment_button.clicked.connect(self.save_experiment)
        update_experiment_button = QPushButton("Update Experiment", self)
        update_experiment_button.clicked.connect(self.update_experiment)
        delete_experiment_button = QPushButton("Delete Experiment", self)
        delete_experiment_button.clicked.connect(self.delete_experiment)

        self.curr_exp_index = 0
        self.experiments_list = [experiment.Experiment("null",
                                                       self.blocks[self.blocks_dropdown.currentText()] if self.blocks else None,
                                                       self.vcfgs[self.vcfgs_dropdown.currentText()] if self.vcfgs else None,
                                                       self.gcode[self.gcode_dropdown.currentText()] if self.gcode else None,
                                                       )]
        if self.enable_adlink:
            self.load_block(self.blocks[self.blocks_dropdown.currentText()])

        self.experiments_tab = QListWidget()
        self.experiments_tab.currentItemChanged.connect(self.exp_index_changed)
        self.experiments_tab.addItems([str(exp) for exp in self.experiments_list])
        self.experiments_tab.setFixedSize(700, 500)
        ############################### WINDOW LAYOUT #################################

        layout_master = QVBoxLayout()

        layout_top = QGridLayout()
        layout_top.addWidget(create_block_button, 0, 0)
        layout_top.addWidget(create_vcfg_button, 0, 1)
        layout_top.addWidget(robot_controls_button, 0, 2)
        layout_top.addWidget(chip_test_button, 0, 3)
        layout_top.addWidget(run_cv_button, 0, 4)
        spacer_top = QSpacerItem(100, 0, QSizePolicy.Policy.Fixed,
                                 QSizePolicy.Policy.Fixed)
        layout_top.addItem(spacer_top, 0, 5)
        layout_top.addWidget(exit_button, 0, 6)
        layout_master.addLayout(layout_top)
        layout_middle = QHBoxLayout()
        layout_middle_grid = QGridLayout()
        layout_middle_grid.addWidget(solution_button, 0, 0)
        layout_middle_grid.addWidget(self.solution_input, 0, 1, 1, 2)
        layout_middle_grid.addWidget(blocks_label, 1, 0)
        layout_middle_grid.addWidget(self.blocks_dropdown, 1, 1)
        layout_middle_grid.addWidget(tile_block_button, 1, 2)
        layout_middle_grid.addWidget(vcfgs_label, 2, 0)
        layout_middle_grid.addWidget(self.vcfgs_dropdown, 2, 1)
        layout_middle_grid.addWidget(gcode_label, 3, 0)
        layout_middle_grid.addWidget(self.gcode_dropdown, 3, 1)
        layout_middle_grid.addWidget(execute_gcode_button, 3, 2)
        layout_middle_grid.addWidget(save_experiment_button, 4, 0)
        layout_middle_grid.addWidget(update_experiment_button, 4, 1)
        layout_middle_grid.addWidget(delete_experiment_button, 4, 2)
        spacer = QSpacerItem(125, 125, QSizePolicy.Policy.Fixed,
                             QSizePolicy.Policy.Minimum)
        layout_middle_grid.addItem(spacer, 5, 0)
        layout_middle_grid.addItem(spacer, 5, 1)
        layout_middle.addLayout(layout_middle_grid)
        layout_middle.addWidget(self.experiments_tab)
        if self.enable_adlink:
            layout_middle.addWidget(self.grid_widget, 0,
                                QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)  # Place the grid widget next to the other widgets
        layout_master.addLayout(layout_middle)

        layout_master.addWidget(
            QLabel(
                f"User: {CONFIG.get('General', 'user')}   Customer: {CONFIG.get('General', 'customer')}   "
                f"Robot On: {self.enable_robot}   PAR On: {self.enable_par}   Counter: {GET_COUNTER_ELECTRODE()}   "
                f"Reference: {GET_REFERENCE_ELECTRODE()}   Working: {GET_WORKING_ELECTRODE()}"
                , self))

        container = QWidget()
        container.setLayout(layout_master)
        self.setCentralWidget(container)

    def enter_solution(self):
        dialog = SolutionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.solution_input.setText(f"{data['cas']}, {data['stock']}, {data['amount']}, {data['concentration']}")
            print(data)  # Add more logic here as needed

    def run_experiments(self):
        index = 0
        for exp in self.experiments_list:
            if self.enable_robot:
                self.execute_gcode(exp.gcode)
            if self.enable_adlink:
                self.load_block(exp.block, True)
            if self.enable_par:
                self.par.cyclic_voltammetry(exp.vcfg, index)

            print("Experiment completed")
            index += 1

    def item_created(self, text):
        if text.split(',')[0].strip() == "Block Created":
            self.blocks = fileio.from_folder(self.blocks_dir, '.block')
            self.blocks_dropdown.clear()
            self.blocks_dropdown.addItems(list(self.blocks.keys()))
            new_index = self.blocks_dropdown.findText(text.split(',')[1].strip())
            self.blocks_dropdown.setCurrentIndex(new_index)
            self.load_block(self.blocks[self.blocks_dropdown.currentText()])
        elif text.split(',')[0].strip() == "CV Config Created":
            self.vcfgs = fileio.from_folder(self.vcfg_dir, '.vcfg')
            self.vcfgs_dropdown.clear()
            self.vcfgs_dropdown.addItems(list(self.vcfgs.keys()))
            new_index = self.vcfgs_dropdown.findText(text.split(',')[1].strip())
            self.vcfgs_dropdown.setCurrentIndex(new_index)

    def chip_test(self, channel):
        for i in range(7):
            match i:
                case 0:
                    chipmap_in = [[0] * 16 for _ in range(64)]
                case 1:
                    chipmap_in = [[1] * 16 for _ in range(64)]
                case 2:
                    chipmap_in = [[2] * 16 for _ in range(64)]
                case 3:
                    chipmap_in = [[3] * 16 for _ in range(64)]
                case 4:
                    chipmap_in = [[1 if (r + c) % 2 == 0 else 2 for c in range(16)] for r in range(64)]
                case 5:
                    chipmap_in = [[2 if (r + c) % 2 == 0 else 3 for c in range(16)] for r in range(64)]
                case 6:
                    chipmap_in = [[random.randint(0, 3) for _ in range(16)] for _ in range(64)]
                case _:
                    break

        self.adlink_card.set_chip_map(channel, chipmap_in)
        chipmap_out = self.adlink_card.get_chip_map(channel)

        for row in range(64):
            for column in range(16):
                self.grid_widget.set_square_color(row, column,
                                                  chipmap_in[row][column], chipmap_out[row][column])

        if chipmap_in == chipmap_out:
            print(f"Test {i} Passed")
        else:
            print(f"Test {i} Failed")
            differences = [
                (r, c, chipmap_in[r][c], chipmap_out[r][c])
                for r in range(len(chipmap_in))
                for c in range(len(chipmap_in[r]))
                if chipmap_in[r][c] != chipmap_out[r][c]
            ]
            for row, col, value1, value2 in differences:
                print(f"Row {row}, Col {col}: chipmap_in has {value1}, chipmap_out has {value2}")

    def execute_gcode(self, gcode):
        gcode_file = os.path.join(self.gcode_dir, gcode.file)
        self.grbl.load_file(gcode_file)
        self.grbl.job_run()

    def tile_block(self):
        self.experiments_list[self.curr_exp_index].tile_block()

        block = self.experiments_list[self.curr_exp_index].block
        self.load_block(block)

    def load_block(self, block, set_card=False):
        # Logic for loading the block
        self.grid_widget.clear()
        current_map = [[0] * 16 for _ in range(64)]
        for i in range(block.num_rows):
            for j in range(block.num_cols):
                current_map[block.start_row + i][block.start_col + j] = block.definition[i][j]
                self.grid_widget.set_square_color(block.start_row + i, block.start_col + j,
                                                  current_map[block.start_row + i][block.start_col + j])
        if set_card:
            self.adlink_card.set_chip_map(1, current_map)

    def exp_index_changed(self, i):  # Not an index, i is a QListWidgetItem
        print(f"Row changed to {self.experiments_tab.row(i)}")
        self.curr_exp_index = self.experiments_tab.row(i)
        if self.curr_exp_index != -1:  # Dont load anything if list is empty
            self.solution_input.setText(self.experiments_list[self.curr_exp_index].solution)
            if self.enable_adlink:
                self.load_block(self.experiments_list[self.curr_exp_index].block)
                index = self.blocks_dropdown.findText(self.experiments_list[self.curr_exp_index].block.name)
                self.blocks_dropdown.setCurrentIndex(index)
            if self.enable_par:
                index = self.vcfgs_dropdown.findText(self.experiments_list[self.curr_exp_index].vcfg.name)
                self.vcfgs_dropdown.setCurrentIndex(index)
            if self.enable_robot:
                index = self.gcode_dropdown.findText(self.experiments_list[self.curr_exp_index].gcode.name)
                self.gcode_dropdown.setCurrentIndex(index)

    def save_experiment(self):
        # TODO: ADD COMPATIBILITY WITH NEW TECHNIQUES
        self.experiments_list.append(
            experiment.Experiment(self.solution_input.text(), self.blocks[
                                                           self.blocks_dropdown.currentText()] if self.blocks else None,
                                                       self.vcfgs[
                                                           self.vcfgs_dropdown.currentText()] if self.vcfgs else None,
                                                       self.gcode[
                                                           self.gcode_dropdown.currentText()] if self.gcode else None,
                                                       ))
        self.experiments_tab.addItem(str(self.experiments_list[-1]))

    def update_experiment(self):
        # TODO: ADD COMPATIBILITY WITH NEW TECHNIQUES
        curr_block = self.experiments_list[self.curr_exp_index].block
        self.experiments_list[self.curr_exp_index] = experiment.Experiment(self.solution_input.text(),
                                                       self.blocks[
                                                           self.blocks_dropdown.currentText()] if self.blocks else None,
                                                       self.vcfgs[
                                                           self.vcfgs_dropdown.currentText()] if self.vcfgs else None,
                                                       self.gcode[
                                                           self.gcode_dropdown.currentText()] if self.gcode else None,
                                                       )
        if curr_block is not None:
            if curr_block.name != self.experiments_list[self.curr_exp_index].block.name:
                self.load_block(self.experiments_list[self.curr_exp_index].block)
            else:
                self.experiments_list[self.curr_exp_index].block = curr_block
        item = self.experiments_tab.item(self.curr_exp_index)
        if item:
            item.setText(str(self.experiments_list[self.curr_exp_index]))

    def delete_experiment(self):
        if self.curr_exp_index == -1:
            return
        del self.experiments_list[self.curr_exp_index]
        self.experiments_tab.clear()
        self.experiments_tab.addItems([str(exp) for exp in self.experiments_list])
