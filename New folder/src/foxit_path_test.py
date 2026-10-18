from foxit_detector import get_active_foxit_file_name
from path_resolver import find_file_in_roots


roots = [

    r"C:\Users\a.motamedolroayafini\Desktop\Local\P-1292\1002"

]


filename = get_active_foxit_file_name()


print("Filename:")
print(filename)


if filename:

    full_path = find_file_in_roots(
        filename,
        roots
    )


    print()
    print("Full path:")
    print(full_path)