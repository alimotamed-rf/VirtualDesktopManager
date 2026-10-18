"""
Task Logger
Tasks Page
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QLabel
)

from PySide6.QtCore import QTimer

from database import DatabaseManager

from datetime import datetime



class TasksPage(QWidget):


    def __init__(self):

        super().__init__()


        self.database = DatabaseManager()


        self.active_key = None


        layout = QVBoxLayout(
            self
        )


        #
        # Filters
        #

        filter_layout = QHBoxLayout()


        self.date_filter = QLineEdit()

        self.date_filter.setPlaceholderText(
            "Date YYYY-MM-DD"
        )


        self.root_filter = QLineEdit()

        self.root_filter.setPlaceholderText(
            "Root"
        )


        self.project_filter = QLineEdit()

        self.project_filter.setPlaceholderText(
            "Project"
        )


        self.apply_button = QPushButton(
            "Apply Filter"
        )


        self.clear_button = QPushButton(
            "Clear"
        )


        filter_layout.addWidget(
            QLabel("Date:")
        )

        filter_layout.addWidget(
            self.date_filter
        )


        filter_layout.addWidget(
            QLabel("Root:")
        )

        filter_layout.addWidget(
            self.root_filter
        )


        filter_layout.addWidget(
            QLabel("Project:")
        )

        filter_layout.addWidget(
            self.project_filter
        )


        filter_layout.addWidget(
            self.apply_button
        )


        filter_layout.addWidget(
            self.clear_button
        )


        layout.addLayout(
            filter_layout
        )


        #
        # Table
        #

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


        self.apply_button.clicked.connect(
            self.refresh
        )


        self.clear_button.clicked.connect(
            self.clear_filters
        )


        self.timer = QTimer()


        self.timer.timeout.connect(
            self.refresh
        )


        self.timer.start(
            1000
        )


        self.refresh()



    def update_active_task(

        self,

        active_key

    ):

        self.active_key = active_key



    def clear_filters(self):

        self.date_filter.clear()

        self.root_filter.clear()

        self.project_filter.clear()

        self.refresh()



    def refresh(self):


        records = self.database.get_projects(

            start_date=self.date_filter.text()
            if self.date_filter.text()
            else None,

            end_date=self.date_filter.text()
            if self.date_filter.text()
            else None,

            root=self.root_filter.text()
            if self.root_filter.text()
            else None,

            project=self.project_filter.text()
            if self.project_filter.text()
            else None

        )


        self.table.setRowCount(
            0
        )


        today = datetime.now().strftime(
            "%Y-%m-%d"
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


            key = root + "|" + project


            values = [

                date,

                root,

                project,

                duration

            ]


            for column, value in enumerate(values):

                self.table.setItem(

                    row,

                    column,

                    QTableWidgetItem(
                        str(value)
                    )

                )


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