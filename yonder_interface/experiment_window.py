import platform
import random
from PyQt6 import QtCore
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QWidget, QDialog, QMainWindow, \
    QApplication, QComboBox, QListWidget, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QDialogButtonBox

from .lib.ui import ui_utils, ROOT_DIR
from .lib.ui.step import Step
from .lib.ui.ui_utils import config_init, load_block_dict, load_vcfg_dict, init_adlink, init_par, init_robot
from .create_block import CreateBlockWindow
from .create_vcfg import CreateVcfgWindow
from .grid_widget import GridWidget
from .robot_window import RobotWindow

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
        return {'cas': self.cas_input.text(), 'stock': self.stock_input.text(), 'amount': self.amount_input.text(),
                'concentration': self.concentration_input.text()}


class ExperimentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CombiMatrixAI")

        config = config_init()

        self.enable_robot = ui_utils.robot_enabled
        self.enable_par = ui_utils.par_enabled
        self.enable_adlink = any(electrode.startswith("Chip: CBMX") for electrode in
                                 [ui_utils.counter_electrode, ui_utils.working_electrode, ui_utils.reference_electrode])

        create_block_button = QPushButton("Create Block", self)
        chip_test_button = QPushButton("Run Chip Test", self)
        blocks_label = QLabel("Load Block:", self)
        self.blocks_dropdown = QComboBox(self)
        tile_block_button = QPushButton("Tile Block", self)
        self.blocks = {}
        if self.enable_adlink:
            if platform.system() != 'Darwin':
                self.adlink_card = init_adlink()

            self.blocks_dir = ROOT_DIR / 'blocks'
            self.blocks = load_block_dict()

            self.create_block_window = CreateBlockWindow()
            self.create_block_window.item_created.connect(self.item_created)

            create_block_button.clicked.connect(self.create_block_window.show)
            chip_test_button.clicked.connect(self.chip_test)

            self.blocks_dropdown.addItems(list(self.blocks.keys()))

            tile_block_button.clicked.connect(self.tile_block)

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

            self.vcfgs = load_vcfg_dict()

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
            if platform.system() != 'Darwin':
                self.grbl = init_robot()
                self.robot_window = RobotWindow(self.grbl)
                robot_controls_button.clicked.connect(self.robot_window.show)

            self.gcode_dir = ROOT_DIR / 'gcode'
            self.gcode = [filename.stem for filename in self.gcode_dir.iterdir()]

            self.gcode_dropdown.addItems(self.gcode)

            execute_gcode_button.clicked.connect(lambda: self.execute_gcode(self.steps_list[self.step_index].gcode))
        else:
            robot_controls_button.setEnabled(False)
            gcode_label.setEnabled(False)
            self.gcode_dropdown.setEnabled(False)
            execute_gcode_button.setEnabled(False)

        run_exp_button = QPushButton("Run Experiment", self)
        run_exp_button.clicked.connect(self.run_experiment)
        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(QApplication.instance().quit)

        solution_button = QPushButton("Enter Solution", self)
        solution_button.clicked.connect(self.enter_solution)
        self.solution_input = QLineEdit(self)
        self.solution_input.setReadOnly(True)

        stage_label = QLabel("Experiment Stage:", self)
        self.stage_dropdown = QComboBox(self)
        self.stage_dropdown.addItems(["Assay", "Clean", "Deposition"])

        save_step_button = QPushButton("New Step", self)
        save_step_button.clicked.connect(self.save_step)
        update_step_button = QPushButton("Update Step", self)
        update_step_button.clicked.connect(self.update_step)
        delete_step_button = QPushButton("Delete Step", self)
        delete_step_button.clicked.connect(self.delete_step)

        self.step_index = -1
        self.steps_list = [
            Step("null", "null", self.blocks[self.blocks_dropdown.currentText()] if self.blocks else None,
                 self.vcfgs[self.vcfgs_dropdown.currentText()] if self.vcfgs else None,
                 self.gcode_dropdown.currentText() if self.gcode else None)]
        if self.enable_adlink:
            self.load_block(self.blocks[self.blocks_dropdown.currentText()])

        self.steps_tab = QListWidget(self)
        self.steps_tab.currentItemChanged.connect(self.step_index_changed)
        self.steps_tab.addItems([str(exp) for exp in self.steps_list])
        self.steps_tab.setFixedSize(700, 500)
        ############################### WINDOW LAYOUT #################################

        layout_master = QVBoxLayout()

        layout_top = QGridLayout()
        layout_top.addWidget(create_block_button, 0, 0)
        layout_top.addWidget(create_vcfg_button, 0, 1)
        layout_top.addWidget(robot_controls_button, 0, 2)
        layout_top.addWidget(chip_test_button, 0, 3)
        layout_top.addWidget(run_exp_button, 0, 4)
        spacer_top = QSpacerItem(100, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
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
        layout_middle_grid.addWidget(stage_label, 4, 0)
        layout_middle_grid.addWidget(self.stage_dropdown, 4, 1)
        layout_middle_grid.addWidget(save_step_button, 5, 0)
        layout_middle_grid.addWidget(update_step_button, 5, 1)
        layout_middle_grid.addWidget(delete_step_button, 5, 2)
        layout_middle.addLayout(layout_middle_grid)
        layout_middle.addWidget(self.steps_tab)
        if self.enable_adlink:
            layout_middle.addWidget(self.grid_widget, 0,
                                    QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)  # Place the grid widget next to the other widgets
        layout_master.addLayout(layout_middle)

        layout_master.addWidget(
            QLabel(f"User: {config.get('General', 'user')}   Customer: {config.get('General', 'customer')}   "
                   f"Robot: {self.enable_robot}   PAR: {self.enable_par}   Counter: {ui_utils.counter_electrode}   "
                   f"Reference: {ui_utils.reference_electrode}   Working: {ui_utils.working_electrode}", self))

        container = QWidget()
        container.setLayout(layout_master)
        self.setCentralWidget(container)

    def run_experiment(self):
        index = 0
        for exp in self.steps_list:
            if self.enable_robot:
                self.execute_gcode(exp.gcode)
            if self.enable_adlink:
                self.load_block(exp.block, True)
            if self.enable_par:
                self.par.cyclic_voltammetry(exp.vcfg, index)

            print("Experiment completed")
            index += 1

    def chip_test(self):
        channel = 1

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
                    self.grid_widget.set_square_color(row, column, chipmap_in[row][column], chipmap_out[row][column])

            if chipmap_in == chipmap_out:
                print(f"Test {i} Passed")
            else:
                print(f"Test {i} Failed")
                differences = [(r, c, chipmap_in[r][c], chipmap_out[r][c]) for r in range(len(chipmap_in)) for c in
                            range(len(chipmap_in[r])) if chipmap_in[r][c] != chipmap_out[r][c]]
                for row, col, value1, value2 in differences:
                    print(f"Row {row}, Col {col}: chipmap_in has {value1}, chipmap_out has {value2}")

    def tile_block(self):
        self.steps_list[self.step_index].tile_block()

        block = self.steps_list[self.step_index].block
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

    def execute_gcode(self, gcode):
        gcode_file = self.gcode_dir / f"{gcode}.gcode"
        self.grbl.load_file(gcode_file)
        self.grbl.job_run()

    def step_index_changed(self, i):  # Not an index, i is a QListWidgetItem
        print(f"Row changed to {self.steps_tab.row(i)}")
        self.step_index = self.steps_tab.row(i)
        if self.step_index != -1:  # Dont load anything if list is empty
            self.solution_input.setText(self.steps_list[self.step_index].solution)
            if self.enable_adlink:
                self.load_block(self.steps_list[self.step_index].block)
                index = self.blocks_dropdown.findText(self.steps_list[self.step_index].block.name)
                self.blocks_dropdown.setCurrentIndex(index)
            if self.enable_par:
                index = self.vcfgs_dropdown.findText(self.steps_list[self.step_index].vcfg.name)
                self.vcfgs_dropdown.setCurrentIndex(index)
            if self.enable_robot:
                index = self.gcode_dropdown.findText(self.steps_list[self.step_index].gcode)
                self.gcode_dropdown.setCurrentIndex(index)

    def item_created(self, text):
        if text.split(',')[0].strip() == "Block Created":
            self.blocks = load_block_dict()
            self.blocks_dropdown.clear()
            self.blocks_dropdown.addItems(list(self.blocks.keys()))
            new_index = self.blocks_dropdown.findText(text.split(',')[1].strip())
            self.blocks_dropdown.setCurrentIndex(new_index)
            self.load_block(self.blocks[self.blocks_dropdown.currentText()])
        elif text.split(',')[0].strip() == "PAR Config Created":
            self.vcfgs = load_vcfg_dict()
            self.vcfgs_dropdown.clear()
            self.vcfgs_dropdown.addItems(list(self.vcfgs.keys()))
            new_index = self.vcfgs_dropdown.findText(text.split(',')[1].strip())
            self.vcfgs_dropdown.setCurrentIndex(new_index)

    def enter_solution(self):
        dialog = SolutionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.solution_input.setText(f"{data['cas']}, {data['stock']}, {data['amount']}, {data['concentration']}")
            print(data)  # Add more logic here as needed

    def save_step(self):
        self.steps_list.append(Step(self.solution_input.text(), self.stage_dropdown.currentText(),
                                    self.blocks[self.blocks_dropdown.currentText()] if self.blocks else None,
                                    self.vcfgs[self.vcfgs_dropdown.currentText()] if self.vcfgs else None,
                                    self.gcode_dropdown.currentText() if self.gcode else None))
        self.steps_tab.addItem(str(self.steps_list[-1]))

    def update_step(self):
        if self.step_index == -1:
            return
        curr_block = self.steps_list[self.step_index].block
        self.steps_list[self.step_index] = Step(self.solution_input.text(), self.stage_dropdown.currentText(),
                                                self.blocks[
                                                    self.blocks_dropdown.currentText()] if self.blocks else None,
                                                self.vcfgs[self.vcfgs_dropdown.currentText()] if self.vcfgs else None,
                                                self.gcode_dropdown.currentText() if self.gcode else None)
        if curr_block is not None:
            if curr_block.name != self.steps_list[self.step_index].block.name:
                self.load_block(self.steps_list[self.step_index].block)
            else:
                self.steps_list[self.step_index].block = curr_block
        item = self.steps_tab.item(self.step_index)
        if item:
            item.setText(str(self.steps_list[self.step_index]))

    def delete_step(self):
        if self.step_index == -1:
            return
        del self.steps_list[self.step_index]
        self.steps_tab.clear()
        self.steps_tab.addItems([str(exp) for exp in self.steps_list])
        self.step_index = -1
