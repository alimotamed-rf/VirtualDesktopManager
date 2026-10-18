import ctypes
import time


user32 = ctypes.windll.user32


def is_workstation_locked():
    """
    Check whether the Windows workstation is currently locked.
    """

    desktop = user32.OpenInputDesktop(
        0,
        False,
        0x0001
    )

    if desktop == 0:
        return True

    user32.CloseDesktop(desktop)

    return False


def main():

    print("Windows Lock Detection Test")
    print("============================")
    print()
    print("Lock your computer with Win + L.")
    print("Then unlock it.")
    print()

    while True:

        if is_workstation_locked():
            status = "LOCKED"
        else:
            status = "UNLOCKED"

        print(
            f"\rWorkstation: {status}",
            end="",
            flush=True
        )

        time.sleep(1)


if __name__ == "__main__":
    main()
