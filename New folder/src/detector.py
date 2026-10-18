"""
WorkLogger
Detector + Timer Runner
"""

import time

from activity_detector import ActivityDetector

from timer_engine import TimerEngine



class Detector:


    def __init__(self):

        self.activity_detector = ActivityDetector()

        self.timer_engine = TimerEngine()


        print("Detector initialized")



    def run(self):

        print("WorkLogger running...")

        print("-" * 60)



        while True:


            activity = self.activity_detector.get_active_activity()



            self.timer_engine.update(activity)



            if activity:


                print(
                    "Application:",
                    activity.application
                )


                print(
                    "Project:",
                    activity.project
                )


            print(
                "Timers:",
                self.timer_engine.get_status()
            )


            print("-" * 60)



            time.sleep(1)