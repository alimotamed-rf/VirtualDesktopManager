import time
import ctypes

from pyvda import VirtualDesktop

import database
import excel_report


class DesktopTracker:

    EXCEL_UPDATE_INTERVAL = 5

    def __init__(self):

        # ---------------------------------------------
        # Initialize database
        # ---------------------------------------------

        database.create_database()

        # Create Excel report if necessary
        excel_report.create_excel_file()

        # ---------------------------------------------
        # Current desktop
        # ---------------------------------------------

        current = VirtualDesktop.current()

        self.current_desktop_number = (
            current.number
        )

        self.current_desktop_name = (
            self.get_desktop_name(current)
        )

        # ---------------------------------------------
        # Timing
        # ---------------------------------------------

        self.last_update_time = time.time()

        self.last_excel_update = time.time()

        self.was_locked = False

    # =================================================
    # DESKTOP NAME
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
    # LOCK DETECTION
    # =================================================

    def is_workstation_locked(self):

        user32 = ctypes.windll.user32

        desktop = user32.OpenInputDesktop(
            0,
            False,
            0x0001
        )

        if desktop == 0:

            return True

        user32.CloseDesktop(desktop)

        return False

    # =================================================
    # CURRENT DESKTOP
    # =================================================

    def get_current_desktop(self):

        return VirtualDesktop.current()

    # =================================================
    # SAVE ELAPSED TIME
    # =================================================

    def save_elapsed_time(self, elapsed):

        if elapsed <= 0:
            return

        database.add_time(
            self.current_desktop_name,
            elapsed
        )

    # =================================================
    # UPDATE EXCEL
    # =================================================

    def update_excel(self):

        try:

            excel_report.write_database_to_excel()

            self.last_excel_update = time.time()

        except Exception as error:

            print(
                f"Excel update error: {error}"
            )

    # =================================================
    # TRACKING TICK
    # =================================================

    def tick(self):

        now = time.time()

        # ---------------------------------------------
        # Check workstation lock
        # ---------------------------------------------

        locked = (
            self.is_workstation_locked()
        )

        if locked:

            if not self.was_locked:

                elapsed = (
                    now
                    - self.last_update_time
                )

                self.save_elapsed_time(
                    elapsed
                )

                self.last_update_time = now

                self.update_excel()

                self.was_locked = True

            return

        # ---------------------------------------------
        # Workstation was unlocked
        # ---------------------------------------------

        if self.was_locked:

            self.last_update_time = now

            self.last_excel_update = now

            self.was_locked = False

            return

        # ---------------------------------------------
        # Detect desktop change
        # ---------------------------------------------

        active_desktop = (
            self.get_current_desktop()
        )

        new_number = (
            active_desktop.number
        )

        new_name = (
            self.get_desktop_name(
                active_desktop
            )
        )

        desktop_switched = (
            new_number
            != self.current_desktop_number
        )

        desktop_renamed = (
            new_name
            != self.current_desktop_name
        )

        # ---------------------------------------------
        # Desktop switched / renamed
        # ---------------------------------------------

        if (
            desktop_switched
            or desktop_renamed
        ):

            elapsed = (
                now
                - self.last_update_time
            )

            self.save_elapsed_time(
                elapsed
            )

            self.current_desktop_number = (
                new_number
            )

            self.current_desktop_name = (
                new_name
            )

            self.last_update_time = now

        # ---------------------------------------------
        # IMPORTANT:
        # Save current elapsed time to SQLite
        # every tick.
        # ---------------------------------------------

        elapsed = (
            now
            - self.last_update_time
        )

        self.save_elapsed_time(
            elapsed
        )

        # Reset timer after saving
        self.last_update_time = now

        # ---------------------------------------------
        # Update Excel every 5 seconds
        # ---------------------------------------------

        if (
            now
            - self.last_excel_update
            >= self.EXCEL_UPDATE_INTERVAL
        ):

            self.update_excel()

    # =================================================
    # STOP
    # =================================================

    def stop(self):

        if self.was_locked:

            return

        now = time.time()

        elapsed = (
            now
            - self.last_update_time
        )

        self.save_elapsed_time(
            elapsed
        )

        self.last_update_time = now

        self.update_excel()