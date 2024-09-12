from PyQt6 import QtWidgets

class GridWidget(QtWidgets.QWidget):
    def __init__(self, size, block_chipmap=None, rows=64, columns=16):
        super().__init__()
        self.block_chipmap = block_chipmap  # Bring the chipmap to this scope
        self.setStyleSheet("background-color: black;")  # Set background color to black
        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setSpacing(1)  # Set spacing between squares
        self.squares = []

        for row in range(rows):
            row_squares = []
            for col in range(columns):
                square = QtWidgets.QLabel(self)
                square.setFixedSize(size, size)  # Set a fixed size for the squares
                square.setStyleSheet("background-color: grey;")
                square.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
                if block_chipmap is not None:
                    square.mousePressEvent = lambda event, r=row, c=col: self.on_square_click(r, c)
                self.grid_layout.addWidget(square, row, col)
                row_squares.append(square)
            self.squares.append(row_squares)

    def set_square_color(self, row, col, value, value_match = None):
        if 0 <= row < len(self.squares) and 0 <= col < len(self.squares[row]):
            if value_match is None:
                match value:
                    case 0:
                        self.squares[row][col].setStyleSheet("background-color: grey;")
                    case 1:
                        self.squares[row][col].setStyleSheet("background-color: blue;")
                    case 2:
                        self.squares[row][col].setStyleSheet("background-color: yellow;")
                    case 3:
                        self.squares[row][col].setStyleSheet("background-color: green;")
            elif value_match is not None:
                match value, value_match:
                    case (0, 0):
                        self.squares[row][col].setStyleSheet("background-color: grey;")
                    case (1, 1):
                        self.squares[row][col].setStyleSheet("background-color: blue;")
                    case (2, 2):
                        self.squares[row][col].setStyleSheet("background-color: yellow;")
                    case (3, 3):
                        self.squares[row][col].setStyleSheet("background-color: green;")
                    case _:
                        self.squares[row][col].setStyleSheet("background-color: red;")


    def on_square_click(self, row, col):
        if self.squares[row][col].styleSheet() == "background-color: grey;":
            self.set_square_color(row, col, 2)
            self.block_chipmap[row][col] = 2
        else:
            self.set_square_color(row, col, 0)
            self.block_chipmap[row][col] = 0

    def clear(self):
        for row in range(64):
            for col in range(16):
                self.set_square_color(row, col, 0)
                if self.block_chipmap is not None:
                    self.block_chipmap[row][col] = 0

