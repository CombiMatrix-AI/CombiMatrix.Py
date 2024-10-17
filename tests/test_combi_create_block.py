import pytest
from pytestqt.qt_compat import qt_api
from pytestqt.qtbot import QtBot

from yonder_interface.launch_window import LaunchWindow
from yonder_interface.lib.ui import ROOT_DIR


@pytest.fixture
def app(qtbot: QtBot):
    """Fixture to initialize the application."""
    window = LaunchWindow()
    qtbot.addWidget(window)
    window.show()
    return qtbot, window


def test_combi_create_block(app):
    """Test to check if Combi Chip screen is open."""
    qtbot, window = app

    qtbot.mouseClick(window.combi_button, qt_api.QtCore.Qt.MouseButton.LeftButton)

    # Validate if the CombiChipScreen is displayed
    assert window.combi_window.isVisible()

    qtbot.mouseClick(window.combi_window.create_block_button, qt_api.QtCore.Qt.MouseButton.LeftButton)

    assert window.combi_window.create_block_window.isVisible()

    qtbot.mouseClick(window.combi_window.create_block_window.grid_widget.squares[1][1], qt_api.QtCore.Qt.MouseButton.LeftButton)
    qtbot.mouseClick(window.combi_window.create_block_window.block_name_input, qt_api.QtCore.Qt.MouseButton.LeftButton)
    qtbot.keyClicks(window.combi_window.create_block_window.block_name_input, 'TestBlockCreate123')
    qtbot.mouseClick(window.combi_window.create_block_window.create_block_button, qt_api.QtCore.Qt.MouseButton.LeftButton)

    file_path = ROOT_DIR / 'data' / 'blocks' / 'TestBlockCreate123.block'

    assert file_path.exists()

    # Delete the file
    try:
        file_path.unlink()
        print("File deleted successfully.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    pytest.main()
