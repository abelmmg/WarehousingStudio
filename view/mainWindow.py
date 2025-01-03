import pandas as pd
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QMainWindow, QAction, QVBoxLayout, QFileDialog, QTreeWidget, QTreeWidgetItem, QWidget, QHBoxLayout, QTableWidgetItem, \
    QSplitter

from view.tableWidget import TableWidget
from view.diagram.dia2 import DiagramWindow
#from view.diagram.diagramWindow import DiagramWindow
from view.tableEditor import TableEditor
from view.treeWidget import TreeWidget


class MainWindow(QMainWindow):
    def __init__(self, req):
        super().__init__()

        self.df = pd.DataFrame(req.req)
        self.interfaces = req.interfaces
        self.applications = req.applications
        #self.df.set_index('ReqId')


        # Create table widget
        self.table = TableWidget(self.df)

        # Create widgets
        self.tree_widget = TreeWidget(req, self.table)

        # Create main layout
        main_layout = QHBoxLayout()
        #main_layout.addWidget(self.tree_widget)
        #main_layout.addWidget(self.table)

        # Create central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tree_widget)
        splitter.addWidget(self.table)
        # Set initial sizes (adjust as needed)
        splitter.setSizes([10, 800])  # Tree width: 200, Table width: 300

        # Set central widget
        self.setCentralWidget(splitter)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 2100, 1500)

        # Create menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')
        file_action = QAction('Open Table', self)
        file_action.triggered.connect(self.open_table)
        file_menu.addAction(file_action)

        # Export menu
        export_menu = menubar.addMenu('Export')
        export_action = QAction('Export Data', self)
        export_action.triggered.connect(self.export_data)
        export_menu.addAction(export_action)

        # Exit menu
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        menubar.addAction(exit_action)

        # Application menu
        application_menu = menubar.addMenu('Application')
        app_action = QAction('Open Diagram', self)
        app_action.triggered.connect(self.open_diagram)
        application_menu.addAction(app_action)

    def open_table(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Excel File', '', 'Excel Files (*.xlsx);;All Files (*)',
                                                  options=options)
        if filename:
            df = pd.read_excel(filename)
            self.table_editor = TableEditor(df)
            self.table_editor.exec_()

    def export_data(self):
        # Placeholder for export functionality
        pass

    def open_diagram(self):
        self.diagram_window = DiagramWindow(self.interfaces, self.applications)
        self.diagram_window.exec_()

