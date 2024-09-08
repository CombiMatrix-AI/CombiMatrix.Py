import os
from PyQt6 import QtWidgets, QtCore


class SetupWindow(QtWidgets.QMainWindow):
    block_created = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup Window")
        self.resize(800, 600)

        self.tab_widget = QtWidgets.QTabWidget(self)

        create_block_tab = QtWidgets.QWidget()
        create_block_layout = QtWidgets.QVBoxLayout(create_block_tab)

        self.block_chipmap = [[0] * 16 for _ in range(64)]
        self.grid_widget = self.ClickableGridWidget(self.block_chipmap)
        create_block_layout.addWidget(self.grid_widget, 0,
                                      QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        self.block_name_input = QtWidgets.QLineEdit(self)
        self.block_name_input.setPlaceholderText("Enter Block Name")
        create_block_layout.addWidget(self.block_name_input, 0,
                                      QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.create_block_button = QtWidgets.QPushButton("Create Block")
        self.create_block_button.clicked.connect(self.create_block)
        create_block_layout.addWidget(self.create_block_button, 0,
                                      QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.tab_widget.addTab(create_block_tab, "Create Block")
        self.setCentralWidget(self.tab_widget)

    def create_block(self):
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

        block_definition = ""
        for row in range(first_row, last_row + 1):
            for col in range(first_col, last_col + 1):
                block_definition += str(self.block_chipmap[row][col])

        block_name = self.block_name_input.text()

        # Create the content for the .block file
        block_file_content = (
            "[Block]\n"
            f"Number rows = {width}\n"
            f"Number columns = {length}\n"
            f"Start row = {first_row}\n"
            f"Start column = {first_col}\n"
            f'Definition = "{block_definition}"\n'
        )

        # Ensure the blocks directory exists
        blocks_dir = os.path.join(os.path.dirname(__file__), '..', 'blocks')

        # Write the content to a .block file in the blocks folder
        with open(os.path.join(blocks_dir, f"{block_name}.block"), "w") as block_file:
            block_file.write(block_file_content)

        self.grid_widget.clear()
        self.block_created.emit("New Block Created")


    class ClickableGridWidget(QtWidgets.QWidget):
        def __init__(self, block_chipmap, rows=64, columns=16):
            super().__init__()
            self.block_chipmap = block_chipmap # Bring the chipmap to this scope
            self.setStyleSheet("background-color: black;")  # Set background color to black
            self.grid_layout = QtWidgets.QGridLayout(self)
            self.grid_layout.setSpacing(1)  # Set spacing between squares
            self.squares = []

            for row in range(rows):
                row_squares = []
                for col in range(columns):
                    square = QtWidgets.QLabel(self)
                    square.setFixedSize(8, 8)  # Set a fixed size for the squares
                    square.setStyleSheet("background-color: grey;")
                    square.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
                    square.mousePressEvent = lambda event, r=row, c=col: self.on_square_click(r, c)
                    self.grid_layout.addWidget(square, row, col)
                    row_squares.append(square)
                self.squares.append(row_squares)

        def on_square_click(self, row, col):
            if self.squares[row][col].styleSheet() == "background-color: grey;":
                self.squares[row][col].setStyleSheet("background-color: yellow;")
                self.block_chipmap[row][col] = 2
            else:
                self.squares[row][col].setStyleSheet("background-color: grey;")
                self.block_chipmap[row][col] = 0

        def clear(self):
            for row in range(64):
                for col in range(16):
                    self.squares[row][col].setStyleSheet("background-color: grey;")
                    self.block_chipmap[row][col] = 0

