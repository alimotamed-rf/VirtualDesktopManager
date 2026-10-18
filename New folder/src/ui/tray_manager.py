"""
Task Logger
System Tray Manager
"""

from PySide6.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
    QApplication
)

from PySide6.QtGui import (
    QAction,
    QIcon,
    QPixmap
)

from PySide6.QtCore import Qt



class TrayManager:


    def __init__(self, window):

        self.window = window


        self.tray = QSystemTrayIcon(
            self.window
        )


        # Temporary visible icon
        pixmap = QPixmap(
            32,
            32
        )

        pixmap.fill(
            Qt.white
        )

        self.tray.setIcon(
            QIcon(pixmap)
        )


        self.menu = QMenu()



        self.open_action = QAction(
            "Open Task Logger",
            self.menu
        )


        self.exit_action = QAction(
            "Exit",
            self.menu
        )



        self.open_action.triggered.connect(
            self.show_window
        )


        self.exit_action.triggered.connect(
            self.exit_app
        )



        self.menu.addAction(
            self.open_action
        )


        self.menu.addSeparator()


        self.menu.addAction(
            self.exit_action
        )


        self.tray.setContextMenu(
            self.menu
        )


        self.tray.activated.connect(
            self.tray_clicked
        )


        self.tray.show()



    def tray_clicked(
        self,
        reason
    ):

        if reason == QSystemTrayIcon.DoubleClick:

            self.show_window()



    def minimize_to_tray(self):

        self.window.hide()


        self.tray.showMessage(

            "Task Logger",

            "Application is running in background",

            QSystemTrayIcon.Information,

            2000

        )



    def show_window(self):

        self.window.show()

        self.window.raise_()

        self.window.activateWindow()



    def exit_app(self):

        if self.window.tracker:

            self.window.tracker.stop()


        self.tray.hide()


        QApplication.quit()