from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class DebugWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 700, 500)
        self.setWindowTitle("Debug Display")

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def write(self, text):
        self.text_edit.append(text.rstrip())
