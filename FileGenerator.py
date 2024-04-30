class FileGenerator():
    def __init__(self,num_processes, num_operations):
        self.num_processes = num_processes
        self.num_operations = num_operations
        self.processes_array = [i for i in range(1,self.num_processes + 1)]

    def generate_new_instruction(self):
        pass

    def generate_use_instruction(self):
        pass

    def generate_delete_instruction(self):
        pass

    def generate_kill_instruction(self):
        pass