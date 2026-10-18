"""
WorkLogger
Foxit PDF Detector
"""

from pywinauto import Desktop


def get_active_foxit_file_name():

    try:

        windows = Desktop(
            backend="uia"
        ).windows()


        for window in windows:

            title = window.window_text()


            if "Foxit PDF Editor" in title:

                filename = title.replace(
                    " - Foxit PDF Editor",
                    ""
                )


                return filename


    except Exception:

        pass


    return None