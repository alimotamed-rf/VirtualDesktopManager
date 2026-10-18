"""
WorkLogger
PDF Detector
"""

import win32com.client


def get_active_pdf_file():

    try:

        foxit = win32com.client.GetActiveObject(
            "FoxitPhantomPDF.Application"
        )

        document = foxit.ActiveDoc


        if document:

            return document.Path


    except Exception:

        pass


    return None