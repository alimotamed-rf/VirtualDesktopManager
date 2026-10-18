import win32com.client


EXCEL_FILE_NAME = "DesktopTimeTracker.xlsx"


def update_open_excel():

    try:
        excel = win32com.client.GetActiveObject("Excel.Application")
    except Exception:
        print("Excel is not currently running.")
        return

    workbook = None

    for wb in excel.Workbooks:

        if wb.Name.lower() == EXCEL_FILE_NAME.lower():
            workbook = wb
            break

    if workbook is None:
        print(f"{EXCEL_FILE_NAME} is not open in Excel.")
        return

    worksheet = workbook.Worksheets("Desktop Time")

    worksheet.Cells(2, 1).Value = "2026-08-13"
    worksheet.Cells(2, 2).Value = "tasklogger"
    worksheet.Cells(2, 3).Value = 5025 / 86400
    worksheet.Cells(2, 3).NumberFormat = "[h]:mm:ss"

    workbook.Save()

    print("Excel workbook updated successfully.")


if __name__ == "__main__":
    update_open_excel()
