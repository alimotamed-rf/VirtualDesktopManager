import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget
)

from ui.settings_page import SettingsPage


class TestWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.resize(800, 600)

        tabs = QTabWidget()

        self.setCentralWidget(tabs)

        settings = SettingsPage()

        tabs.addTab(
            settings,
            "Settings"
        )


app = QApplication(sys.argv)

window = TestWindow()

window.show()

sys.exit(app.exec())