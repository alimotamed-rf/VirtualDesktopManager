import win32com.client


try:

    acad = win32com.client.GetActiveObject("AutoCAD.Application")

    print("AutoCAD connected")

    doc = acad.ActiveDocument

    print("Drawing:")
    print(doc.FullName)


except Exception as e:

    print("Error:")
    print(e)