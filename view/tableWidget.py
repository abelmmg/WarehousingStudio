from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QStyle, \
    QStyledItemDelegate, QHeaderView
from PyQt5.QtCore import Qt


class TableWidget(QTableWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.init_ui()

    def init_ui(self):
        # Create table widget
        self.setColumnCount(len(self.data.columns))  # Include 'Process' column
        # self.setHorizontalHeaderLabels(list(self.data.columns)[0:])  # Set header labels
        self.setHorizontalHeaderLabels(self.data.columns)

        # Set combobox for "Included" column
        self.setItemDelegateForColumn(5, ComboBoxDelegate(self))

        self.cellChanged.connect(self.on_table_cell_changed)  # Connect to cellChanged signal

    def update_ui(self, data):
        # Update table widget
        self.data = data
        self.setColumnCount(len(self.data.columns))  # Include 'Process' column
        # self.setHorizontalHeaderLabels(list(self.data.columns)[0:])  # Set header labels
        self.setHorizontalHeaderLabels(self.data.columns)
        self.cellChanged.connect(self.on_table_cell_changed)  # Connect to cellChanged signal

    def on_table_cell_changed(self, row, column):
        # Get the updated value from the table
        #pass
        # Set background color for "TBD"
        item_tbd = self.item(row, 5)
        if item_tbd:
            if item_tbd.text() == "TBD":
                color = QColor(Qt.red)
                item_tbd.setBackground(color)
            if item_tbd.text() == "Yes":
                color = QColor(Qt.green)
                item_tbd.setBackground(color)
            if item_tbd.text() == "No":
                color = QColor(Qt.transparent)
                item_tbd.setBackground(color)
            if item_tbd.text() == "GAP":
                color = QColor(Qt.gray)
                item_tbd.setBackground(color)

    def update_table(self, records, current_df):

        if self.rowCount() > 0:
            # Update dataset
            index_column = current_df.columns.size - 1
            len_df = len(current_df)
            for row in range(self.rowCount()):
                index_value = int(self.item(row, index_column).text())
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    if item:
                        new_value = item.text()
                        column_name = current_df.columns[col]
                        if index_value < len_df:
                            print(index_value)
                            current_df.iloc[index_value, col] = new_value

        # Clear existing table contents
        self.setRowCount(0)
        self.update_ui(records)

        # Populate the table with new data
        for index, row in records.iterrows():
            row_position = self.rowCount()
            ##row_position = row['ReqId2']
            self.insertRow(row_position)
            for col, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                # Enable word wrap for the cell
                item.setFlags(item.flags() | Qt.TextWordWrap)
                self.setItem(row_position, col, item)
                ##self.table.setItem(row_position, col, QTableWidgetItem(str(value)))

        # Resize columns to fit content
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        # Resize rows to fit content
        self.resizeRowsToContents()

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = ["Yes", "No", "GAP", "TBD"]

    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(self.items)
        return editor

    def setEditorData(self, editor, index):
        index = self.parent().model().index(index.row(), index.column())
        value = index.data(Qt.DisplayRole)
        editor.setCurrentText(str(value))

    def setModelData(self, editor, model, index):
        index = self.parent().model().index(index.row(), index.column())
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)
