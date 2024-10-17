import faulthandler
import sys

from PyQt6.QtWidgets import QApplication

from yonder_interface.launch_window import LaunchWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    faulthandler.enable()

    window = LaunchWindow()
    window.show()
    window.raise_()
    window.activateWindow()

    sys.exit(app.exec())
