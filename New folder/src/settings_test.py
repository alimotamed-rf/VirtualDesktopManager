import sys

from PySide6.QtWidgets import QApplication

from ui.settings_page import SettingsPage


app = QApplication(sys.argv)

window = SettingsPage()

window.show()

sys.exit(app.exec())