from autocad_detector import get_autocad_active_file


print("AutoCAD detector test")

path = get_autocad_active_file()


if path:

    print("Active DWG:")
    print(path)

else:

    print("No AutoCAD drawing detected")