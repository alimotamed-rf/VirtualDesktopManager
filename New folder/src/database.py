"""
Task Logger
Database Manager
"""

import os
import sqlite3
import sys
from datetime import datetime


class DatabaseManager:

    def __init__(self):

        self.db_path = self.get_database_path()

        os.makedirs(
            os.path.dirname(self.db_path),
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

        print("Database connected.")

    def get_base_path(self):

        if getattr(sys, "frozen", False):

            return os.path.dirname(
                sys.executable
            )

        return os.path.abspath(

            os.path.join(

                os.path.dirname(__file__),

                ".."

            )

        )

    def get_database_path(self):

        return os.path.join(

            self.get_base_path(),

            "data",

            "worklogger.db"

        )

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS work_log(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            work_date TEXT,

            root TEXT,

            project TEXT,

            seconds REAL,

            last_update TEXT,

            UNIQUE(work_date, root, project)

        )

        """)

        self.connection.commit()

    def update_project_time(

        self,

        work_date,

        root,

        project,

        seconds

    ):

        self.cursor.execute("""

        INSERT INTO work_log
        (
            work_date,
            root,
            project,
            seconds,
            last_update
        )

        VALUES
        (?,?,?,?,datetime('now'))

        ON CONFLICT(work_date,root,project)

        DO UPDATE SET

            seconds=?,

            last_update=datetime('now')

        """,

        (

            work_date,

            root,

            project,

            seconds,

            seconds

        )

        )

        self.connection.commit()

    def get_today_projects(self, work_date):

        self.cursor.execute(

            """
            SELECT
                work_date,
                root,
                project,
                seconds,
                last_update
            FROM work_log
            WHERE work_date = ?
            ORDER BY root, project
            """,

            (work_date,)

        )

        return self.cursor.fetchall()

    def get_all_projects(self):

        self.cursor.execute(

            """
            SELECT
                work_date,
                root,
                project,
                seconds,
                last_update
            FROM work_log
            ORDER BY work_date DESC,
                     root,
                     project
            """

        )

        return self.cursor.fetchall()

    def load_today_projects(self):

        today = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute(

            """
            SELECT
                root,
                project,
                seconds
            FROM work_log
            WHERE work_date = ?
            """,

            (today,)

        )

        return self.cursor.fetchall()

    def get_projects(

        self,

        start_date=None,

        end_date=None,

        root=None,

        project=None

    ):

        query = """

        SELECT

            work_date,

            root,

            project,

            seconds,

            last_update

        FROM work_log

        WHERE 1=1

        """

        params = []

        if start_date:

            query += " AND work_date >= ?"

            params.append(start_date)

        if end_date:

            query += " AND work_date <= ?"

            params.append(end_date)

        if root:

            query += " AND root = ?"

            params.append(root)

        if project:

            query += " AND project = ?"

            params.append(project)

        query += """

        ORDER BY

            work_date DESC,

            root,

            project

        """

        self.cursor.execute(
            query,
            params
        )

        return self.cursor.fetchall()