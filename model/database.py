import pandas as pd


class Database:
    def __init__(self):
        excel_data = pd.read_excel('C:\\Users\\abelm\\PycharmProjects\\WarehousingStudio\\model\\Requirements.xlsx',
                                   sheet_name=None)

        self.connection = ''
        self.processes = excel_data['Processes']
        self.sub_processes = excel_data['SubProcesses']
        self.inventory = excel_data['Inventory']
        self.inbound = excel_data['Inbound']
        self.outbound = excel_data['Outbound']

        self.requirements = pd.concat([self.inventory, self.inbound], ignore_index=True)
        self.requirements = pd.concat([self.requirements, self.outbound], ignore_index=True)

        self.requirements['ReqId'] = self.requirements['Id_Process'] * 10000000 + self.requirements['Id_Sub_Process'] * 10000 + self.requirements['Id_Detail']
        #self.requirements['ReqId2'] = self.requirements['ReqId']
        #self.requirements.set_index('ReqId', inplace=True)

        self.requirements['counter'] = range(1, len(self.requirements) + 1)
        self.requirements['counter2'] = self.requirements['counter']
        self.requirements.set_index('counter', inplace=True)
        ##print(self.requirements.info())

        self.interfaces = excel_data['Interfaces']
        self.interfaces['counter'] = range(1, len(self.interfaces) + 1)
        self.interfaces['counter2'] = self.interfaces['counter']
        self.interfaces.set_index('counter', inplace=True)

        self.applications = excel_data['Applications']
        self.applications['counter'] = range(1, len(self.applications) + 1)
        self.applications['counter2'] = self.applications['counter']
        self.applications.set_index('counter', inplace=True)

    def load_processes(self):
        return self.processes

    def load_sub_processes(self):
        return self.sub_processes

    def get_requirements(self):
        return self.requirements

    def get_applications(self):
        return self.applications

    def get_interfaces(self):
        return self.interfaces
