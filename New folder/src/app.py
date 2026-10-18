import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

from initializer import Initializer

def main():
    Initializer.initialize()
    app = QApplication(sys.argv)

    app.setApplicationName(
        "Task Logger"
    )

    app.setApplicationVersion(
        "1.0.0"
    )


    window = MainWindow()

    window.show()


    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()