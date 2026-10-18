"""
Task Logger
Tasks Page
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem
)

from PySide6.QtCore import QTimer

from database import DatabaseManager
from datetime import datetime



class TasksPage(QWidget):


    def __init__(self):

        super().__init__()


        self.database = DatabaseManager()


        layout = QVBoxLayout(
            self
        )


        self.table = QTableWidget()


        self.table.setColumnCount(
            5
        )


        self.table.setHorizontalHeaderLabels(

            [
                "Date",
                "Root",
                "Project",
                "Time",
                "Status"
            ]

        )


        self.table.horizontalHeader().setStretchLastSection(True)


        layout.addWidget(
            self.table
        )


        self.active_key = None


        self.timer = QTimer()


        self.timer.timeout.connect(
            self.refresh
        )


        self.timer.start(1000)


        self.refresh()



    def update_active_task(

        self,

        active_key

    ):

        self.active_key = active_key



    def refresh(self):


        records = self.database.get_projects()


        self.table.setRowCount(
            0
        )


        for record in records:


            date, root, project, seconds, last_update = record


            row = self.table.rowCount()


            self.table.insertRow(
                row
            )


            seconds = int(seconds)


            hours = seconds // 3600

            minutes = (seconds % 3600) // 60

            secs = seconds % 60


            duration = (
                f"{hours:02}:"
                f"{minutes:02}:"
                f"{secs:02}"
            )


            values = [

                date,

                root,

                project,

                duration

            ]


            key = root + "|" + project


            for column, value in enumerate(values):

                self.table.setItem(

                    row,

                    column,

                    QTableWidgetItem(
                        str(value)
                    )

                )


            today = datetime.now().strftime("%Y-%m-%d")


            if date == today and key == self.active_key:

                status = "🟢 Active"

            elif date == today:

                status = "Paused"

            else:

                status = "Archived"


            self.table.setItem(

                row,

                4,

                QTableWidgetItem(
                    status
                )

            )