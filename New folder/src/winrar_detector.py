"""
WorkLogger
WinRAR Detector
"""

from pywinauto import Desktop


def get_active_winrar_file_name():

    try:

        windows = Desktop(
            backend="uia"
        ).windows()


        for window in windows:

            title = window.window_text()


            if title.lower().endswith(
                (".rar", ".zip", ".7z")
            ):

                return title



    except Exception:


        pass



    return None