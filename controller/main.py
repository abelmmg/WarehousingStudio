
import sys

from PyQt5.QtWidgets import QApplication

from model.requirements import Requirements
from view.mainWindow import MainWindow

if __name__ == '__main__':

    # Loading data
    req = Requirements()

    # Win application
    app = QApplication(sys.argv)
    main_window = MainWindow(req)
    main_window.show()
    sys.exit(app.exec_())
