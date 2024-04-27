class FileProcessor:
    def __init__(self):
        # Initialize any necessary attributes
        pass

    def process_instruction(self, instruction, parameters):
        # Perform different actions based on the instruction and parameters
        if instruction == "new":
            self.handle_new_instruction(parameters)
        elif instruction == "use":
            self.handle_use_instruction(parameters)
        elif instruction == "delete":
            self.handle_delete_instruction(parameters)
        elif instruction == "kill":
            self.handle_kill_instruction(parameters)
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

    def process_file(self, file_path):
        # Read the file line by line and process each instruction
        with open(file_path, 'r') as file:
            for line in file:
                instruction, *parameters = line.strip().split('(')
                parameters = parameters[0].strip(')').split(',')
                self.process_instruction(instruction, parameters)

