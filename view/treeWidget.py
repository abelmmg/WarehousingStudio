from PyQt5.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QTreeWidgetItem, QTableWidgetItem


class TreeWidget(QWidget):
    def __init__(self, req, table):
        super().__init__()

        self.req = req
        self.df = self.req.req
        self.current_df = self.df
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['Processes'])  # Customize header label
        self.tree.itemClicked.connect(self.on_tree_item_clicked)  # Connect to itemClicked signal
        self.table = table  # Store a reference to the table

        self.init_ui()

    def init_ui(self):
        self.create_tree()

        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def create_tree(self):
        ##root_nodes = self.df[~self.df['Process'].isin(self.df['Subprocess'])]['Process'].unique()
        root_nodes = self.df['Process'].unique()

        for root in root_nodes:
            root_item = QTreeWidgetItem([root])
            self.tree.addTopLevelItem(root_item)
            self.add_children(root_item, root)

        root_sol = QTreeWidgetItem(['Solutions'])
        self.tree.addTopLevelItem(root_sol)
        child = 'Applications'
        child_item = QTreeWidgetItem([child])
        root_sol.addChild(child_item)

        child = 'Interfaces'
        child_item = QTreeWidgetItem([child])
        root_sol.addChild(child_item)

    def add_children(self, parent_item, parent_process):
        ##children = self.df[self.df['Process'] == parent_process]['Subprocess'].tolist()
        children = self.df[self.df['Process'] == parent_process]['Subprocess'].unique()
        for child in children:
            child_item = QTreeWidgetItem([child])
            parent_item.addChild(child_item)
            self.add_children(child_item, child)

    def on_tree_item_clicked(self, item, column):
        # Get the selected process from the clicked item
        selected_process = item.text(0)

        if selected_process not in ('Applications', 'Interfaces'):
            # Filter the DataFrame to get associated records
            associated_records = self.df[
                (self.df['Process'] == selected_process) |
                (self.df['Subprocess'] == selected_process)]
            self.update_table(associated_records)
            self.current_df = self.df
        else:
            if selected_process == 'Interfaces':
                # Filter the DataFrame to get associated records
                associated_records = self.req.interfaces
                self.update_table(associated_records)
                self.current_df = self.req.interfaces
            else:
                associated_records = self.req.applications
                self.update_table(associated_records)
                self.current_df = self.req.applications





    def update_table(self, records):

        if self.table.rowCount() > 0:
            # Update dataset
            index_column = self.current_df.columns.size - 1
            len_df = len(self.current_df)
            for row in range(self.table.rowCount()):
                index_value = int(self.table.item(row, index_column).text())
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        new_value = item.text()
                        column_name = self.current_df.columns[col]
                        if index_value < len_df:
                            print(index_value)
                            self.current_df.iloc[index_value, col] = new_value

        # Clear existing table contents
        self.table.setRowCount(0)
        self.table.update_ui(records)

        # Populate the table with new data
        for index, row in records.iterrows():
            row_position = self.table.rowCount()
            ##row_position = row['ReqId2']
            self.table.insertRow(row_position)
            for col, value in enumerate(row):
                self.table.setItem(row_position, col, QTableWidgetItem(str(value)))
