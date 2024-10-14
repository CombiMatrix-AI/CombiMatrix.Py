import pytest
from pytestqt.qt_compat import qt_api
from pytestqt.qtbot import QtBot

from app import LaunchWindow


@pytest.fixture
def app(qtbot: QtBot):
    """Fixture to initialize the application."""
    window = LaunchWindow()
    qtbot.addWidget(window)
    window.show()
    return qtbot, window


def test_combi_chip_screen_is_open(app):
    """Test to check if Combi Chip screen is open."""
    qtbot, window = app

    qtbot.mouseClick(window.combi_button, qt_api.QtCore.Qt.MouseButton.LeftButton)

    # Validate if the CombiChipScreen is displayed
    assert window.combi_window.isVisible()

    qtbot.mouseClick(window.combi_window.create_block_button, qt_api.QtCore.Qt.MouseButton.LeftButton)

    assert window.combi_window.create_block_window.isVisible()


if __name__ == "__main__":
    pytest.main()
