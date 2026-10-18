"""
Task Logger
Background Tracker Service
"""

import time
import pythoncom

from PySide6.QtCore import QThread, Signal

from activity_detector import ActivityDetector
from timer_engine import TimerEngine



class TrackerService(QThread):


    activity_updated = Signal(object, object)



    def __init__(self):

        super().__init__()

        self.running = True

        self.activity_detector = ActivityDetector()

        self.timer_engine = TimerEngine()

        self.active_key = None



    def run(self):

        pythoncom.CoInitialize()

        try:

            while self.running:


                activity = (
                    self.activity_detector
                    .get_active_activity()
                )


                self.timer_engine.update(
                    activity
                )


                if activity and activity.root and activity.project:

                    self.active_key = (

                        activity.root
                        +
                        "|"
                        +
                        activity.project

                    )

                else:

                    self.active_key = None



                self.activity_updated.emit(

                    self.timer_engine.get_status(),

                    self.active_key

                )


                time.sleep(1)

        finally:

            pythoncom.CoUninitialize()


    def stop(self):

        self.running = False

        self.quit()

        self.wait()
