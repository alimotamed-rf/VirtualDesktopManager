"""
WorkLogger
Unified Activity Detector

Detects:
- Windows Explorer folders
- AutoCAD drawings
- Foxit PDF tabs
- Outlook files
- WinRAR archives
- Other applications using process detection
"""

import win32gui
import win32process
import psutil
import win32com.client


from file_detector import get_active_file_path

from autocad_detector import get_autocad_active_file

from foxit_detector import get_active_foxit_file_name

from outlook_detector import get_active_outlook_file_name

from winrar_detector import get_active_winrar_file_name

from path_resolver import find_file_in_roots

from project_mapper import find_project

from models import Activity



# =====================================================
# Tracked folders
# =====================================================

TRACKED_ROOTS = [

    r"C:\Users\a.motamedolroayafini\Desktop\Local\P-1292\1002"

]



class ActivityDetector:


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



        application_lower = application.lower()



        # =====================================================
        # AutoCAD
        # =====================================================

        if application_lower == "acad.exe":

            path = get_autocad_active_file()



        # =====================================================
        # Foxit PDF
        # =====================================================

        elif "foxit" in application_lower:


            filename = get_active_foxit_file_name()


            if filename:

                path = find_file_in_roots(

                    filename,

                    TRACKED_ROOTS

                )



        # =====================================================
        # Outlook
        # =====================================================

        elif "outlook" in application_lower:


            filename = get_active_outlook_file_name()


            if filename:

                path = find_file_in_roots(

                    filename,

                    TRACKED_ROOTS

                )



        # =====================================================
        # WinRAR
        # =====================================================

        elif "winrar" in application_lower:


            filename = get_active_winrar_file_name()


            if filename:

                path = find_file_in_roots(

                    filename,

                    TRACKED_ROOTS

                )



        # =====================================================
        # Other applications
        # =====================================================

        else:


            path = get_active_file_path(pid)



        # =====================================================
        # Windows Explorer folder detection
        # =====================================================

        if path is None:

            path = self.get_explorer_path(hwnd)



        # =====================================================
        # Project mapping
        # =====================================================

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





    # =====================================================
    # Explorer folder detector
    # =====================================================

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





    # =====================================================
    # Folder check
    # =====================================================

    def is_folder(self, path):


        import os


        if path:


            return os.path.isdir(path)



        return False