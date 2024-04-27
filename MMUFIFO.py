import math
from Process import Process
from Pointer import Pointer
from Page import Page
#from queue import Queue


class MMUFIFO():
    def __init__(self):
        #This is in kb
        self.RAM = 40
        self.PAGE_SIZE  = 4
        self.current_memory = 0
        self.pointer_id_generator = 0
        self.page_id_generator = 0
        self.pointer_page_map = {}
        self.processes = []
        self.fifo_queue = []
    
    def process_new_command(self,pid,size):
        kb_size = size / 1000
        num_pages = math.ceil(kb_size / 4)
        print("Num pages: ",num_pages)
        #Gets the process if it already exists, if not, then returns a new one
        process = self.get_process(pid)
        #Creates the new pointer
        new_pointer = self.create_pointer()
        #Adds the pointer to the list of the process
        process.add_pointer(new_pointer)
        for i in range(0,num_pages):
            self.page_id_generator += 1
            if self.current_memory + self.PAGE_SIZE > self.RAM:
                memory_segment = self.replace_page()
                new_page = Page(memory_segment,self.page_id_generator)
            else:
                self.current_memory += self.PAGE_SIZE
                new_page = Page(self.current_memory,self.page_id_generator)
            self.pointer_page_map[self.pointer_id_generator].append(new_page)
            self.fifo_queue.append(new_page)
    
    def process_use_command(self, pointer_id):
        process = get_process_by_pointer(pointer_id)

    def process_delete_command(self,pointer_id):
        process = get_process_by_pointer(pointer_id)

    def process_kill_command(self,pid):
        process = self.processes.remove(pid)
        pointers = process.get_pointers()
        for pointer in pointers:
            del self.pointer_page_map[pointer.get_pointer_id()]

    
    def get_process_by_pointer(self, pointer_id):
        for proc in self.process:
            if is_pointer_process(pointer_id):
                return proc
        raise Exception("Coudln't find pointer")
    
    def get_process(self, id):
        for proc in self.processes:
            if proc.get_process_id() == id:
                return proc
        process = Process(id)
        self.processes.append(process)
        return process
    
    def create_pointer(self):
        self.pointer_id_generator += 1
        new_pointer_id = self.pointer_id_generator 
        new_pointer = Pointer(new_pointer_id)
        if self.pointer_id_generator not in self.pointer_page_map:
            self.pointer_page_map[self.pointer_id_generator] = []
        return new_pointer
    
    def replace_page(self):
        if not len(self.fifo_queue) == 0:
            page = self.fifo_queue.pop(0)
            page.set_in_ram()
            return page.get_segment()

    #You can use this to debug
    def print_map(self):
        for l in self.pointer_page_map.values():
            for val in l:
                val.print_page()

    #Print process pointers
    def print_processes_pointers(self):
        for proc in self.processes:
            print("Process ID is: ",proc.get_process_id())
            proc.print_pointers()
            print("-------------------------------------")


    def print_queue(self):
        for i in self.fifo_queue:
            i.print_page()