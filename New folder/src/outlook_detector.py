"""
WorkLogger
Outlook Detector
"""

from pywinauto import Desktop


def get_active_outlook_file_name():

    try:

        windows = Desktop(
            backend="uia"
        ).windows()


        for window in windows:


            title = window.window_text()


            if " - Message" in title:


                return title



    except Exception:


        pass



    return None