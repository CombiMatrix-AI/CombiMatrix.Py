######################################################################################
# Main UI control of app
######################################################################################
import sys
import configparser
from PyQt6 import QtWidgets
from qt_material import apply_stylesheet

import view.mainwindow

if __name__ == "__main__":
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read/Access values from the configuration file
    config.read("config.ini")
    theme = config.get('General', 'theme')

    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme=theme)
    main_window = view.mainwindow.MainWindow()
    main_window.show()
    app.exec()

