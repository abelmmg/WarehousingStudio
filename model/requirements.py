from model.database import Database
import pandas as pd


class Requirements:
    def __init__(self):
        self.data = Database()
        self.req = self.data.get_requirements()
        self.interfaces = self.data.get_interfaces()
        self.applications = self.data.get_applications()
        """
        self.processes = self.data.load_processes()
        self.sub_processes = self.data.load_sub_processes()
        """

    def save_data(self, filename):
        """
          Saves DataFrames to different sheets in an Excel file.

          Args:
            filename: Path and filename for the Excel file.
        """
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            self.applications.to_excel(writer, sheet_name='Applications', index=False)
            self.interfaces.to_excel(writer, sheet_name='Interfaces', index=False)

            ware = self.req[self.req['Process'] == 'Warehouse']
            inve = self.req[self.req['Process'] == 'Inventory']
            inbo = self.req[self.req['Process'] == 'Inbound']
            outb = self.req[self.req['Process'] == 'Outbound']
            ware.to_excel(writer, sheet_name='Warehouse', index=False)
            inve.to_excel(writer, sheet_name='Inventory', index=False)
            inbo.to_excel(writer, sheet_name='Inbound', index=False)
            outb.to_excel(writer, sheet_name='Outbound', index=False)

    def assign_project(self, project_name, customer_name):
        self.req["Project"] = project_name
        self.req["Customer"] = customer_name

        self.interfaces["Project"] = project_name
        self.interfaces["Customer"] = customer_name

        self.applications["Project"] = project_name
        self.applications["Customer"] = customer_name
