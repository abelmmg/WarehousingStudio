import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QFileDialog, QTreeWidget, QTreeWidgetItem, QWidget, \
    QHBoxLayout, QTableWidgetItem, \
    QSplitter, QMessageBox, QInputDialog

from model.requirements import Requirements
from view.tableWidget import TableWidget
from view.diagram.diagramWindow import DiagramWindow
#from view.diagram.diagramWindow import DiagramWindow
from view.tableEditor import TableEditor
from view.treeWidget import TreeWidget


class MainWindow(QMainWindow):
    def __init__(self, req:Requirements):
        super().__init__()

        self.req = req
        self.df = pd.DataFrame(req.req)
        self.interfaces = req.interfaces
        self.applications = req.applications

        # Create table widget
        self.table = TableWidget(self.df)

        # Create Tree widget
        self.tree_widget = TreeWidget(req, self.table)

        # Create main layout
        main_layout = QHBoxLayout()
        # Create central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree_widget)
        splitter.addWidget(self.table)
        # Set initial sizes (adjust as needed)
        splitter.setSizes([10, 800])  # Tree width: 10, Table width: 800
        # Set central widget
        self.setCentralWidget(splitter)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 2100, 1500)
        self.showMaximized()

        # Create menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')
        file_action = QAction('New Project', self)
        file_action.triggered.connect(self.new_project)
        file_menu.addAction(file_action)

        file_action = QAction('Save Project', self)
        file_action.triggered.connect(self.save_project)
        file_menu.addAction(file_action)

        file_action = QAction('Load Project', self)
        file_action.triggered.connect(self.load_project)
        file_menu.addAction(file_action)

        # Application menu
        application_menu = menubar.addMenu('Application')
        app_action = QAction('Open Diagram', self)
        app_action.triggered.connect(self.open_diagram)
        application_menu.addAction(app_action)

        # Exit menu
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        menubar.addAction(exit_action)

        # Load the icon from a file
        icon_path = "../resources/warehouse-bn1.png"
        self.setWindowIcon(QIcon(icon_path))

    def new_project(self):
        project_name, ok = QInputDialog.getText(None, "New Project", "Enter the Project Name:")
        if ok and project_name:
            customer_name, ok = QInputDialog.getText(None, "New Project", "Enter the Customer Name:")
            if ok and customer_name:
                self.req.assign_project(project_name, customer_name)

    def save_project(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "Project Files (*.xlsx)")
        if filename:
            try:
                with open(filename, 'wb') as f:
                    self.req.save_data(filename)
                    QMessageBox.information(self, "Success", "Project saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save project: {e}")

    def open_diagram(self):
        self.diagram_window = DiagramWindow(self.interfaces, self.applications)
        self.diagram_window.exec_()

    def load_project(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Project", "", "Project Files (*.xlsx)")
        if filename:
            try:
                with open(filename, 'wb') as f:
                    self.req.save_data(filename)
                    QMessageBox.information(self, "Success", "Project loaded successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load project: {e}")
