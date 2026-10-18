"""
Task Logger
Unified Activity Detector
"""

import os

import psutil
import win32com.client
import win32gui
import win32process

from autocad_detector import get_autocad_active_file
from file_detector import get_active_file_path
from foxit_detector import get_active_foxit_file_name
from models import Activity
from path_resolver import find_file_in_roots
from project_mapper import find_project
from settings_manager import SettingsManager
from winrar_detector import get_active_winrar_file_name


class ActivityDetector:

    def __init__(self):

        self.settings = SettingsManager()

    def get_tracked_roots(self):

        return self.settings.get_roots()

    def get_active_activity(self):

        hwnd = win32gui.GetForegroundWindow()

        if hwnd == 0:
            return None

        title = win32gui.GetWindowText(hwnd)

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        try:

            process = psutil.Process(pid)

            application = process.name()

        except Exception:

            application = "Unknown"

        path = None

        roots = self.get_tracked_roots()

        app = application.lower()

        # AutoCAD

        if app == "acad.exe":

            path = get_autocad_active_file()

        # Foxit

        elif "foxit" in app:

            filename = get_active_foxit_file_name()

            if filename:

                path = find_file_in_roots(

                    filename,

                    roots

                )

        # WinRAR

        elif "winrar" in app:

            filename = get_active_winrar_file_name()

            if filename:

                path = find_file_in_roots(

                    filename,

                    roots

                )

        # Other applications

        else:

            path = get_active_file_path(pid)

        # Explorer

        if path is None:

            path = self.get_explorer_path(hwnd)

        project_info = None

        if path:

            project_info = find_project(path)

        if project_info:

            root = project_info["root"]

            project = project_info["project"]

        else:

            root = None

            project = None

        return Activity(

            application=application,

            title=title,

            path=path,

            root=root,

            project=project,

            is_folder=self.is_folder(path)

        )

    def get_explorer_path(self, hwnd):

        try:

            shell = win32com.client.Dispatch(

                "Shell.Application"

            )

            for window in shell.Windows():

                if int(window.HWND) == hwnd:

                    return window.Document.Folder.Self.Path

        except Exception:

            pass

        return None

    def is_folder(self, path):

        if path:

            return os.path.isdir(path)

        return False