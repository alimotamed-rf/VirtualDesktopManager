"""
Task Logger
Timer Engine
"""

from datetime import datetime

from database import DatabaseManager
from excel_exporter import ExcelExporter


class TimerEngine:

    def __init__(self):

        self.last_time = datetime.now()

        self.database = DatabaseManager()

        self.excel = ExcelExporter()

        self.projects = {}

        #
        # Restore today's timers
        #

        for root, project, seconds in self.database.load_today_projects():

            key = root + "|" + project

            self.projects[key] = {

                "root": root,

                "project": project,

                "seconds": float(seconds)

            }

        print("Timer Engine initialized")


    def update(self, activity):

        now = datetime.now()

        delta = (now - self.last_time).total_seconds()

        self.last_time = now

        if activity is None:
            return

        if activity.project is None:
            return

        if activity.root is None:
            return

        key = activity.root + "|" + activity.project

        #
        # New project today
        #

        if key not in self.projects:

            self.projects[key] = {

                "root": activity.root,

                "project": activity.project,

                "seconds": 0.0

            }

        #
        # Continue counting
        #

        self.projects[key]["seconds"] += delta

        #
        # Save to database
        #

        self.database.update_project_time(

            work_date=now.strftime("%Y-%m-%d"),

            root=activity.root,

            project=activity.project,

            seconds=self.projects[key]["seconds"]

        )

        #
        # Update Excel
        #

        self.excel.export(self.projects)


    def get_status(self):

        return self.projects