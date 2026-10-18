"""
Task Logger
Dashboard Page
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)

from PySide6.QtCore import Qt


class DashboardPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Task Logger")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet(
            "font-size:24px;font-weight:bold;"
        )

        layout.addWidget(title)

        self.status = QLabel(
            "Status: Starting..."
        )

        self.status.setAlignment(Qt.AlignCenter)

        layout.addWidget(
            self.status
        )

        self.active_task = QLabel(
            "No active task"
        )

        self.active_task.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            self.active_task
        )

        self.tray_button = QPushButton(
            "Minimize to Tray"
        )

        layout.addWidget(
            self.tray_button
        )

        layout.addStretch()


    def update_status(
        self,
        active_key
    ):

        self.status.setText(
            "🟢 Tracker Running"
        )

        if active_key:

            self.active_task.setText(
                active_key
            )

        else:

            self.active_task.setText(
                "No active task"
            )