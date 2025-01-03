from model.database import Database


class Requirements:
    def __init__(self):
        self.data = Database()
        self.req = self.data.get_requirements()
        self.interfaces = self.data.get_interfaces()
        self.applications = self.data.get_applications()
        self.processes = self.data.load_processes()
        self.sub_processes = self.data.load_sub_processes()


