from PyQt5.QtWidgets import QTableWidget, QWidget


class TableWidget(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.init_ui()

    def init_ui(self):
        # Create table widget
        #self.table = QTableWidget()
        ##self.table.setColumnCount(2)  # Adjust column count as needed
        ##self.table.setHorizontalHeaderLabels(['Column 1', 'Column 2'])  # Set header labels
        ##self.table.setColumnCount(len(self.df.columns) - 1)  # Exclude 'Process' column
        self.setColumnCount(len(self.df.columns))  # Include 'Process' column
        self.setHorizontalHeaderLabels(list(self.df.columns)[0:])  # Set header labels
        self.cellChanged.connect(self.on_table_cell_changed)  # Connect to cellChanged signal

    def update_ui(self, dataframe):
        # Update table widget
        self.df = dataframe
        self.setColumnCount(len(self.df.columns))  # Include 'Process' column
        self.setHorizontalHeaderLabels(list(self.df.columns)[0:])  # Set header labels
        self.cellChanged.connect(self.on_table_cell_changed)  # Connect to cellChanged signal

    def on_table_cell_changed(self, row, column):
        # Get the updated value from the table
        return 0
        updated_value = self.item(row, column).text()
        idx_value = self.item(row, 16)

        # Update the DataFrame using the 'counter' column for indexing
        l = self.df.columns.get_loc('counter2')
        counter_value = self.df.iloc[row, l] - 1  # Adjust for zero-based indexing
        self.df.loc[self.df['counter2'] == counter_value, self.df.columns[column]] = updated_value


        if idx_value is not None:

                #updated_value = self.item(row, column).text()
                print('update value: ' + updated_value.text())
                # Get the corresponding process from the DataFrame
                #process = self.df.iloc[row, 0]  # Assuming 'Process' is the first column

                print(row)
                #print(column)
                #print('process value: ' + process)
                #index_value = self.df.iloc[row, 16].round().astype(int)   #.astype('int64')
                index_value = self.df.iloc[idx_value, 16]

                print('index value: ' + str(index_value))
                # Update the DataFrame
                ##self.df.iloc[row, column] = updated_value  # Adjust column index due to 'Process' column
                ##self.df.loc[idx, column] = updated_value

                # Column name
                column_name = self.df.columns[column]

                # Update the cell value using .at
                self.df.at[index_value, column_name] = updated_value.text()
                print(column_name)