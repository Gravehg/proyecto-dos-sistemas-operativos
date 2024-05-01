import random
class FileGeneratorProcess():
    def __init__(self):
        self.pointers = []
        


class FileGenerator():
    def __init__(self,num_processes, num_operations, seed):
        random.seed(int(seed))
        self.num_processes = num_processes
        self.num_operations = num_operations
        self.active_processes_array = [i for i in range(1,self.num_processes + 1)]
        self.can_be_killed = []
        self.process_pointer_map = {}
        for process in self.active_processes_array:
            self.process_pointer_map[process] = []
        self.active_pointers_array = []
        self.instructions = ["new","use","delete","kill"]
        self.pointers = 1

    def generate_file(self):
      with open("generated.txt", 'w') as file:
        for _ in range(0,self.num_operations):
            instruction = random.choice(self.instructions)
            if instruction == "new" and self.active_processes_array:
                #Chooses a process that hasnt been killed
                process = random.choice(self.active_processes_array)
                print("selected process new: ", process)
                size = random.randint(10000,40000)
                file.write(f"new({process},{size})\n")                  
                self.process_pointer_map[process].append(self.pointers)
                if not process in self.can_be_killed:
                    self.can_be_killed.append(process)
                self.active_pointers_array.append(self.pointers)
                self.pointers += 1
            elif instruction == "use" and self.active_pointers_array:
                pointer = random.choice(self.active_pointers_array)
                file.write(f"use({pointer})\n")
            elif instruction == "delete" and self.active_pointers_array:
                pointer = random.choice(self.active_pointers_array)
                self.active_pointers_array.remove(pointer)
                file.write(f"delete({pointer})\n")
            elif instruction == "kill" and self.can_be_killed:
                process = random.choice(self.can_be_killed)
                print("Killing process: ", process)
                pointer_list = self.process_pointer_map[process]
                self.active_processes_array.remove(process)
                self.can_be_killed.remove(process)
                for pointer in pointer_list:
                    if pointer in self.active_pointers_array:
                        self.active_pointers_array.remove(pointer)
                del self.process_pointer_map[process]
                file.write(f"kill({process})\n")
        while self.can_be_killed:
            file.write(f"kill({self.can_be_killed.pop(0)})\n")       
        return file
      
    def get_key_by_value(self,value):
        for key, lst in self.process_pointer_map.item():
            if value in lst:
                return key
