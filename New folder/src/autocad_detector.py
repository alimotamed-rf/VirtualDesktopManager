"""
WorkLogger
AutoCAD Detector
"""

import win32com.client


def get_autocad_active_file():

    try:

        acad = win32com.client.GetActiveObject(
            "AutoCAD.Application"
        )

        document = acad.ActiveDocument

        if document:

            filepath = document.FullName

            if filepath:

                return filepath


    except Exception:

        pass


    return None