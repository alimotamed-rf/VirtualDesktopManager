"""
Task Logger
Main Application Window
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget
)

from PySide6.QtCore import QTimer


from tracker_service import TrackerService


from ui.dashboard_page import DashboardPage

from ui.tasks_page import TasksPage

from ui.settings_page import SettingsPage

from ui.tray_manager import TrayManager



class MainWindow(QMainWindow):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "Task Logger"
        )


        self.resize(
            1200,
            800
        )


        #
        # Tabs
        #

        self.tabs = QTabWidget()

        self.setCentralWidget(
            self.tabs
        )



        #
        # Pages
        #

        self.dashboard_page = DashboardPage()

        self.tasks_page = TasksPage()

        self.settings_page = SettingsPage()

        self.tray_manager = TrayManager(self)



        self.tabs.addTab(

            self.dashboard_page,

            "Dashboard"

        )


        self.tabs.addTab(

            self.tasks_page,

            "Tasks"

        )


        self.tabs.addTab(

            self.settings_page,

            "Settings"

        )



        #
        # Tracker
        #

        self.tracker = None

        self.dashboard_page.tray_button.clicked.connect(

            self.tray_manager.minimize_to_tray

        )



        QTimer.singleShot(

            1000,

            self.start_tracker

        )



    def start_tracker(self):


        self.tracker = TrackerService()


        self.tracker.activity_updated.connect(

            self.update_ui

        )


        self.tracker.start()



    def update_ui(

        self,

        data,

        active_key

    ):


        self.dashboard_page.update_status(

            active_key

        )


        self.tasks_page.update_active_task(

            active_key

        )



    def closeEvent(self, event):


        if self.tracker:

            self.tracker.stop()


        event.accept()