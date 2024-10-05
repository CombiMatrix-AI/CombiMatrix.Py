import os
from PyQt6 import QtWidgets, QtCore

from definitions import ROOT_DIR
from view.grid_widget import GridWidget


class CreateBlockWindow(QtWidgets.QMainWindow):
    item_created = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Block")

        create_block_widget = QtWidgets.QWidget()
        create_block_layout = QtWidgets.QHBoxLayout(create_block_widget)

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

        self.setCentralWidget(create_block_widget)

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
        blocks_dir = os.path.join(ROOT_DIR, 'blocks')

        # Write the content to a .block file in the blocks folder
        with open(os.path.join(blocks_dir, f"{block_name}.block"), "w") as block_file:
            block_file.write(block_file_content)

        self.grid_widget.clear()
        self.item_created.emit(f"Block Created, {block_name}")
