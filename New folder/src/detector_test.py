import time
import win32gui
import win32process
import psutil
import win32com.client

from project_mapper import find_project
from file_detector import get_active_file_path
from autocad_detector import get_autocad_active_file

def get_active_window_info():

    hwnd = win32gui.GetForegroundWindow()

    if hwnd == 0:
        return None

    window_title = win32gui.GetWindowText(hwnd)

    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        process = psutil.Process(pid)
        process_name = process.name()

    except Exception:
        process_name = "Unknown"


    folder_path = get_explorer_path(hwnd)


    return {
    "application": process_name,
    "title": window_title,
    "folder": folder_path,
    "pid": pid
}



def get_explorer_path(hwnd):

    try:

        shell = win32com.client.Dispatch("Shell.Application")

        for window in shell.Windows():

            if int(window.HWND) == hwnd:

                return window.Document.Folder.Self.Path

    except Exception:
        pass


    return None



print("WorkLogger Detector v0.4 started...")
print("Press Ctrl + C to stop")
print("-" * 70)



while True:

    info = get_active_window_info()


    if info:

        print(
            "Application:",
            info["application"]
        )

        print(
            "Title:",
            info["title"]
        )


        if info["folder"]:

            print(
                "Folder:",
                info["folder"]
            )
        else:

            if info["application"].lower() == "acad.exe":

                file_path = get_autocad_active_file()

else:

    file_path = get_active_file_path(
        info["pid"]
    )

    if file_path:

                print(
                    "File:",
                    file_path
                )

                project = find_project(file_path)

                if project:

                    print(
                        "ROOT:",
                        project["root"]
                    )

                    print(
                        "PROJECT:",
                        project["project"]
                    )

                else:

                    print(
                        "PROJECT: Not tracked"
                    )


                project = find_project(info["folder"])


    if project:

                print(
                    "ROOT:",
                    project["root"]
                )

                print(
                    "PROJECT:",
                    project["project"]
                )

    else:

                print(
                    "PROJECT: Not tracked"
                )

print("-" * 70)


time.sleep(1)