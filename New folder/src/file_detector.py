"""
Task Logger
Active File Detector
"""

import win32gui
import win32process
import psutil
import os


def get_foreground_title():

    hwnd = win32gui.GetForegroundWindow()

    if hwnd:

        return win32gui.GetWindowText(hwnd)

    return ""



def extract_file_from_title(title):

    if not title:

        return None


    extensions = [

        ".xlsx",
        ".xls",
        ".docx",
        ".doc",
        ".pptx",
        ".ppt",
        ".txt"

    ]


    title = title.strip()


    for ext in extensions:

        if ext.lower() in title.lower():

            parts = title.split(" - ")


            for part in parts:

                if ext.lower() in part.lower():

                    return part.strip()


    return None



def find_file_in_process(pid, filename):

    try:

        process = psutil.Process(pid)


        for open_file in process.open_files():

            if os.path.basename(open_file.path) == filename:

                return open_file.path


    except Exception:

        pass


    return None



def get_active_file_path(pid):


    title = get_foreground_title()


    filename = extract_file_from_title(
        title
    )


    if not filename:

        return None


    path = find_file_in_process(

        pid,

        filename

    )


    return path