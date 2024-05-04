from MMUFIFO import MMUFIFO
from MMUSC import MMUSecondChance
from MMUNRD import MMURND
from MMUMRU import MMUMRU
from MMUOptimal import MMUOptimal

class FileProcessor:
    def __init__(self, file_path, name_algorithm):
        # Initialize any necessary attributes
        self.selected_mmu = None
        print(name_algorithm)
        if name_algorithm == "FIFO":
            self.selected_mmu = MMUFIFO()
        elif name_algorithm == "SC":
            self.selected_mmu = MMUSecondChance()
        elif name_algorithm == "RND":
            self.selected_mmu = MMURND()
        elif name_algorithm == "MRU":
            self.selected_mmu = MMUMRU()
        self.optimal_mmu = MMUOptimal()
        self.instruction_list = []
        self.path = file_path
        self.read_file_instructions(self.path)
        self.feed_opt_references()

    #Deberia llamarse cada cierto tiempo para que ejecute la instruccion siguiente y se actualice la interfaz
    def process_instruction_mmu(self, instruction, parameters):
        # Perform different actions based on the instruction and parameters
        if instruction == "new":
            pid, size = parameters
            self.optimal_mmu.process_new_command(int(pid), int(size))
            self.selected_mmu.process_new_command(int(pid), int(size))
        elif instruction == "use":
            pointer_id = parameters[0]
            self.optimal_mmu.process_use_command(int(pointer_id))
            self.selected_mmu.process_use_command(int(pointer_id))
        elif instruction == "delete":
            pointer_id = parameters[0]
            self.optimal_mmu.process_delete_command(int(pointer_id))
            self.selected_mmu.process_delete_command(int(pointer_id))   
        elif instruction == "kill":
            pid = parameters[0]
            self.optimal_mmu.process_kill_command(int(pid))
            self.selected_mmu.process_kill_command(int(pid))
        # Add more conditions for other instructions as needed

    def handle_new_instruction(self, parameters):
        # Process the 'new' instruction
        pid, size = parameters
        print(f"Creating new process with PID: {pid} and size: {size}")

    def handle_use_instruction(self, parameters):
        # Process the 'use' instruction
        pid = parameters[0]
        print(f"Using process with PID: {pid}")

    def handle_delete_instruction(self, parameters):
        # Process the 'delete' instruction
        pid = parameters[0]
        print(f"Deleting process with PID: {pid}")

    def handle_kill_instruction(self, parameters):
        # Process the 'kill' instruction
        pids = parameters
        for pid in pids:
            print(f"Killing process with PID: {pid}")

    # Add more methods to handle other instructions

    def read_file_instructions(self, file_path):
        # Read the file line by line and process each instruction
        with open(file_path, 'r') as file:
            for line in file:
                self.instruction_list.append(line)

    def feed_opt_references(self):
        for line in self.instruction_list:
            instruction, *parameters = line.strip().split('(')
            parameters = parameters[0].strip(')').split(',')
            if instruction == "use":
                self.optimal_mmu.pointer_references.append(int(parameters[0]))

    def process_instruction(self):
        line = self.instruction_list.pop(0)
        instruction, *parameters = line.strip().split('(')
        parameters = parameters[0].strip(')').split(',')
        self.process_instruction_mmu(instruction, parameters)


