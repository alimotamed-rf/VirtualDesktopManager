"""
Task Logger
Settings Page
"""

import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QAbstractItemView
)

from settings_manager import SettingsManager


class SettingsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.settings = SettingsManager()

        layout = QVBoxLayout(self)

        self.folder_list = QListWidget()
        self.folder_list.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        layout.addWidget(self.folder_list)

        self.add_button = QPushButton("Add Directory")
        layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Selected")
        layout.addWidget(self.remove_button)

        self.save_button = QPushButton("Save Settings")
        layout.addWidget(self.save_button)

        self.add_button.clicked.connect(self.add_folder)
        self.remove_button.clicked.connect(self.remove_folder)
        self.save_button.clicked.connect(self.save)

        self.load()

    def load(self):

        self.folder_list.clear()

        for root in self.settings.get_roots():
            self.folder_list.addItem(root)

    def add_folder(self):

        dialog = QFileDialog(self)

        dialog.setFileMode(QFileDialog.Directory)

        dialog.setOption(
            QFileDialog.ShowDirsOnly,
            True
        )

        # IMPORTANT:
        # Use Qt's own dialog instead of the native Windows dialog.
        dialog.setOption(
            QFileDialog.DontUseNativeDialog,
            True
        )

        dialog.setWindowTitle(
            "Select Tracked Root Folder"
        )

        if dialog.exec():

            folder = dialog.selectedFiles()[0]

            folder = os.path.normpath(folder)

            existing = [

                self.folder_list.item(i).text()

                for i in range(
                    self.folder_list.count()
                )

            ]

            if folder not in existing:

                self.folder_list.addItem(folder)

            else:

                QMessageBox.information(

                    self,

                    "Task Logger",

                    "This directory already exists."

                )

    def remove_folder(self):

        item = self.folder_list.currentItem()

        if item:

            self.folder_list.takeItem(

                self.folder_list.row(item)

            )

    def save(self):

        roots = [

            self.folder_list.item(i).text()

            for i in range(
                self.folder_list.count()
            )

        ]

        self.settings.set_roots(roots)

        QMessageBox.information(

            self,

            "Task Logger",

            "Settings saved."

        )