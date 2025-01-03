from PyQt5.QtWidgets import QTableWidget, QDialog, QVBoxLayout, QPushButton, QTableWidgetItem, QMessageBox


class TableEditor(QDialog):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Table Editor')
        self.setGeometry(100, 100, 800, 600)

        # Create table widget
        self.table_widget = QTableWidget(self)
        self.load_table_data()

        # Create buttons
        self.edit_button = QPushButton('Edit Table', self)
        self.save_button = QPushButton('Save Table', self)
        self.edit_button.clicked.connect(self.edit_table)
        self.save_button.clicked.connect(self.save_table)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def load_table_data(self):
        self.table_widget.setRowCount(self.df.shape[0])
        self.table_widget.setColumnCount(self.df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(self.df.columns)

        for row in range(self.df.shape[0]):
            for col in range(self.df.shape[1]):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(self.df.iat[row, col])))

    def edit_table(self):
        self.table_widget.setEditTriggers(QTableWidget.AllEditTriggers)

    def save_table(self):
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        for row in range(self.df.shape[0]):
            for col in range(self.df.shape[1]):
                self.df.iat[row, col] = self.table_widget.item(row, col).text()
        self.df.to_excel('updated_table.xlsx', index=False)
        QMessageBox.information(self, 'Success', 'Table saved to updated_table.xlsx')