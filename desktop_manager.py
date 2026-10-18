import sys
import openpyxl

from pathlib import Path
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from desktop_tracker import DesktopTracker
from datetime import timedelta
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QTabWidget,
    QFrame,
    QInputDialog,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)


class VirtualDesktopManager(QMainWindow):

    # =================================================
    # SYSTEM TRAY
    # =================================================

    def minimize_to_tray(self):

        self.hide()


    def show_from_tray(self):

        self.show()
        self.showNormal()
        self.activateWindow()
        self.raise_()


    def tray_icon_activated(
        self,
        reason
    ):

        if reason == QSystemTrayIcon.DoubleClick:

            self.show_from_tray()


    def exit_application(self):

        self.tracker.stop()

        self.tray_icon.hide()

        QApplication.quit()

    # =================================================
    # CLOSE APPLICATION
    # =================================================

    def closeEvent(self, event):

        # Closing the window minimizes to tray.
        # The tracker continues running.

        event.ignore()

        self.minimize_to_tray()

    # =================================================
    # APPLICATION UPDATE
    # =================================================

    def update_application(self):

        # Update tracking
        self.tracker.tick()

        # Update workspace information
        self.refresh_desktops()

        # Update current workspace
        self.current_desktop.setText(
            self.tracker.current_desktop_name
        )

        # Update history if visible
        if self.tabs.currentIndex() == 1:
            self.load_history()

    # =================================================
    # AUTOMATIC HISTORY REFRESH
    # =================================================

    def auto_refresh_history(self):

        # Only refresh when HISTORY is visible
        if self.tabs.currentIndex() == 1:
            self.load_history()

    # =================================================
    # LOAD HISTORY FROM EXCEL
    # =================================================

    def load_history(self):

        import database

        try:

            database.create_database()

            rows = database.get_all_totals()

        except Exception as error:

            print(
                f"History loading error: {error}"
            )

            return

        # -------------------------------------------------
        # Preserve current selections
        # -------------------------------------------------

        current_date = (
            self.date_filter.currentText()
        )

        current_desktop = (
            self.desktop_filter.currentText()
        )

        # -------------------------------------------------
        # Build filter values directly from SQLite
        # -------------------------------------------------

        dates = sorted(
            {
                str(row[0])
                for row in rows
                if row[0] is not None
            },
            reverse=True
        )

        desktops = sorted(
            {
                str(row[1])
                for row in rows
                if row[1] is not None
            }
        )

        self.date_filter.blockSignals(True)
        self.desktop_filter.blockSignals(True)

        self.date_filter.clear()
        self.date_filter.addItem("All Dates")
        self.date_filter.addItems(dates)

        self.desktop_filter.clear()
        self.desktop_filter.addItem("All Desktops")
        self.desktop_filter.addItems(desktops)

        # -------------------------------------------------
        # Restore filters
        # -------------------------------------------------

        date_index = (
            self.date_filter.findText(
                current_date
            )
        )

        if date_index >= 0:

            self.date_filter.setCurrentIndex(
                date_index
            )

        desktop_index = (
            self.desktop_filter.findText(
                current_desktop
            )
        )

        if desktop_index >= 0:

            self.desktop_filter.setCurrentIndex(
                desktop_index
            )

        self.date_filter.blockSignals(False)
        self.desktop_filter.blockSignals(False)

        # -------------------------------------------------
        # SQLite is now the source of truth
        # -------------------------------------------------

        self.history_rows = rows

        self.apply_history_filter()

    # =================================================
    # FILTER HISTORY
    # =================================================
    def apply_history_filter(self):

        if not hasattr(
            self,
            "history_rows"
        ):
            return

        selected_date = (
            self.date_filter.currentText()
        )

        selected_desktop = (
            self.desktop_filter.currentText()
        )

        filtered_rows = []

        for row in self.history_rows:

            date_value = (
                str(row[0])
                if row[0] is not None
                else ""
            )

            desktop_value = (
                str(row[1])
                if row[1] is not None
                else ""
            )

            if (
                selected_date != "All Dates"
                and date_value != selected_date
            ):
                continue

            if (
                selected_desktop != "All Desktops"
                and desktop_value != selected_desktop
            ):
                continue

            filtered_rows.append(row)

        # -------------------------------------------------
        # Fill table
        # -------------------------------------------------

        self.history_table.setRowCount(
            len(filtered_rows)
        )

        for row_index, row in enumerate(
            filtered_rows
        ):

            date_value = (
                str(row[0])
                if row[0] is not None
                else ""
            )

            desktop_value = (
                str(row[1])
                if row[1] is not None
                else ""
            )

            # SQLite stores time as seconds.
            total_seconds = int(
                float(row[2])
            )

            hours = (
                total_seconds // 3600
            )

            minutes = (
                (total_seconds % 3600)
                // 60
            )

            seconds = (
                total_seconds % 60
            )

            time_value = (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )

            self.history_table.setItem(
                row_index,
                0,
                QTableWidgetItem(
                    date_value
                )
            )

            self.history_table.setItem(
                row_index,
                1,
                QTableWidgetItem(
                    desktop_value
                )
            )

            self.history_table.setItem(
                row_index,
                2,
                QTableWidgetItem(
                    time_value
                )
            )
        

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virtual Desktop Manager")
        self.resize(1100, 700)

        self.desktop_numbers = []

        self.create_ui()
        # =============================================
        # System tray
        # =============================================

        icon_path = Path(__file__).resolve().parent / "icons" / "app.ico"

        self.tray_icon = QSystemTrayIcon(
            QIcon(str(icon_path)),
            self
        )

        self.tray_menu = QMenu()

        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show_from_tray)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_application)

        self.tray_menu.addAction(show_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(
            self.tray_menu
        )

        self.tray_icon.activated.connect(
            self.tray_icon_activated
        )

        self.tray_icon.show()

        # =============================================
        # Tracker
        # =============================================

        self.tracker = DesktopTracker()

        # =============================================
        # UI update timer
        # =============================================

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_application)
        self.timer.start(1000)

        self.refresh_desktops()
        self.load_history()
        # Refresh history every 5 seconds
        self.history_timer = QTimer(self)
        self.history_timer.timeout.connect(self.auto_refresh_history)
        self.history_timer.start(5000)

    # =================================================
    # UI
    # =================================================

    def create_ui(self):

        self.tabs = QTabWidget()

        # =================================================
        # WORKSPACES
        # =================================================

        workspaces = QWidget()
        workspace_layout = QHBoxLayout(workspaces)

        # -------------------------------------------------
        # LEFT PANEL
        # -------------------------------------------------

        left_panel = QFrame()
        left_panel.setFixedWidth(320)

        left_layout = QVBoxLayout(left_panel)

        title = QLabel("WORKSPACES")
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        self.desktop_list = QListWidget()

        # Double-click → rename
        self.desktop_list.itemDoubleClicked.connect(
            self.open_selected_desktop
        )

        new_button = QPushButton("+ New Desktop")
        new_button.clicked.connect(
            self.create_desktop
        )

        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(
            self.open_selected_desktop
        )

        self.rename_button = QPushButton("Rename")
        self.rename_button.clicked.connect(
            self.rename_selected_desktop
        )

        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(
            self.remove_selected_desktop
        )

        left_layout.addWidget(title)
        left_layout.addWidget(new_button)
        left_layout.addWidget(self.desktop_list)

        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(self.open_button)
        buttons_layout.addWidget(self.rename_button)

        left_layout.addLayout(buttons_layout)
        left_layout.addWidget(self.remove_button)

        # -------------------------------------------------
        # RIGHT PANEL
        # -------------------------------------------------

        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)

        current_title = QLabel(
            "CURRENT WORKSPACE"
        )

        self.current_desktop = QLabel("")

        self.current_desktop.setStyleSheet(
            "font-size: 28px; font-weight: bold;"
        )

        right_layout.addWidget(current_title)
        right_layout.addWidget(
            self.current_desktop
        )
        right_layout.addStretch()

        workspace_layout.addWidget(
            left_panel
        )

        workspace_layout.addWidget(
            right_panel
        )

        # =================================================
        # HISTORY
        # =================================================

        history = QWidget()
        history_layout = QVBoxLayout(history)

        history_title = QLabel("HISTORY")

        history_title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        # -------------------------------------------------
        # Filters
        # -------------------------------------------------

        filters_layout = QHBoxLayout()

        self.date_filter = QComboBox()
        self.date_filter.addItem("All Dates")

        self.desktop_filter = QComboBox()
        self.desktop_filter.addItem("All Desktops")

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(
            self.load_history
        )

        filters_layout.addWidget(
            QLabel("Date:")
        )

        filters_layout.addWidget(
            self.date_filter
        )

        filters_layout.addWidget(
            QLabel("Desktop:")
        )

        filters_layout.addWidget(
            self.desktop_filter
        )

        filters_layout.addWidget(
            refresh_button
        )

        filters_layout.addStretch()

        history_layout.addLayout(
            filters_layout
        )

        # -------------------------------------------------
        # History table
        # -------------------------------------------------

        self.history_table = QTableWidget()

        self.history_table.setColumnCount(3)

        self.history_table.setHorizontalHeaderLabels(
            [
                "Date",
                "Desktop",
                "Total Time"
            ]
        )

        self.history_table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        self.history_table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        self.history_table.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        self.history_table.setAlternatingRowColors(True)

        history_layout.addWidget(
            self.history_table
        )

        # Filters trigger table update
        self.date_filter.currentTextChanged.connect(
            self.apply_history_filter
        )

        self.desktop_filter.currentTextChanged.connect(
            self.apply_history_filter
        )

        # =================================================
        # TABS
        # =================================================

        self.tabs.addTab(
            workspaces,
            "WORKSPACES"
        )

        self.tabs.addTab(
            history,
            "HISTORY"
        )

        self.setCentralWidget(
            self.tabs
        )

    # =================================================
    # GET DESKTOP NAME
    # =================================================

    def get_desktop_name(self, desktop):

        name = getattr(
            desktop,
            "name",
            None
        )

        if name and name.strip():

            return name.strip()

        return (
            f"Desktop {desktop.number}"
        )

    # =================================================
    # REFRESH
    # =================================================

    def refresh_desktops(self):

        from pyvda import (
            VirtualDesktop,
            get_virtual_desktops
        )

        desktops = get_virtual_desktops()

        current = VirtualDesktop.current()

        # Remember currently selected desktop
        selected_row = (
            self.desktop_list.currentRow()
        )

        self.desktop_list.clear()

        self.desktop_numbers = []

        for index, desktop in enumerate(
            desktops
        ):

            name = self.get_desktop_name(
                desktop
            )

            self.desktop_numbers.append(
                desktop.number
            )

            text = name

            if (
                desktop.number
                == current.number
            ):

                text += "  ●"

            item = QListWidgetItem(text)

            # Store desktop number inside item
            item.setData(
                256,
                desktop.number
            )

            self.desktop_list.addItem(
                item
            )

            if (
                desktop.number
                == current.number
            ):

                self.current_desktop.setText(
                    name
                )

        # Restore selection when possible
        if (
            selected_row >= 0
            and selected_row
            < self.desktop_list.count()
        ):

            self.desktop_list.setCurrentRow(
                selected_row
            )



    # =================================================
    # CREATE
    # =================================================

    def create_desktop(self):

        from pyvda import VirtualDesktop

        try:
            new_desktop = VirtualDesktop.create()

            # Switch to the newly created desktop
            if new_desktop:
                new_desktop.go()

            self.refresh_desktops()

        except Exception as error:
            print(f"Create error: {error}")

    # =================================================
    # OPEN
    # =================================================

    def open_selected_desktop(self):

        row = self.desktop_list.currentRow()

        if row < 0:
            return

        from pyvda import get_virtual_desktops

        desktops = get_virtual_desktops()

        if row >= len(desktops):
            return

        try:
            desktops[row].go()
            self.refresh_desktops()

        except Exception as error:
            print(f"Open error: {error}")

    # =================================================
    # RENAME
    # =================================================

    def rename_selected_desktop(
        self,
        item=None
    ):

        row = (
            self.desktop_list.currentRow()
        )

        if row < 0:
            return

        from pyvda import get_virtual_desktops

        desktops = get_virtual_desktops()

        if row >= len(desktops):
            return

        desktop = desktops[row]

        old_name = self.get_desktop_name(
            desktop
        )

        new_name, ok = QInputDialog.getText(
            self,
            "Rename Desktop",
            "Desktop name:",
            text=old_name
        )

        if not ok:
            return

        new_name = new_name.strip()

        if not new_name:
            return

        try:

            desktop.rename(new_name)

            self.refresh_desktops()

        except Exception as error:

            print(
                f"Rename error: {error}"
            )

    # =================================================
    # REMOVE
    # =================================================

    def remove_selected_desktop(self):

        from PySide6.QtWidgets import QMessageBox
        from pyvda import get_virtual_desktops, VirtualDesktop

        row = self.desktop_list.currentRow()

        if row < 0:
            return

        desktops = get_virtual_desktops()

        if row >= len(desktops):
            return

        desktop = desktops[row]

        current = VirtualDesktop.current()

        name = self.get_desktop_name(desktop)

        # Do not allow removing the current desktop
        if desktop.number == current.number:

            QMessageBox.warning(
                self,
                "Cannot Remove",
                "You cannot remove the current workspace.\n\n"
                "Switch to another workspace first."
            )

            return

        reply = QMessageBox.question(
            self,
            "Remove Workspace",
            f"Remove '{name}'?\n\n"
            "This will remove the Windows virtual desktop.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:

            desktop.remove()

            self.refresh_desktops()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Remove Error",
                str(error)
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = VirtualDesktopManager()

    window.show()

    sys.exit(
        app.exec()
    )