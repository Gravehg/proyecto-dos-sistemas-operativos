import math
from Process import Process
from Pointer import Pointer
from Page import Page
#from queue import Queue


class MMUFIFO():
    def __init__(self):
        #This is in kb
        #It should be 400, 40 for testing purposes
        self.RAM = 40
        self.PAGE_SIZE  = 4
        self.FRAME_NUM = self.RAM // 4
        self.available_addresses = [i * self.PAGE_SIZE for i in range(self.FRAME_NUM)]
        self.current_memory_usage = 0
        self.pointer_id_generator = 0
        self.page_id_generator = 0
        self.pointer_page_map = {}
        self.processes = []
        self.fifo_queue = []
    
    def allocate_page(self):
        if not self.available_addresses:
            return None  # No available pages left
        return self.available_addresses.pop(0)

    def process_new_command(self,pid,size):
        kb_size = size / 1000
        num_pages = math.ceil(kb_size / 4)
        #Gets the process if it already exists, if not, then returns a new one
        process = self.get_process(pid)
        #Creates the new pointer
        new_pointer = self.create_pointer()
        #Adds the pointer to the list of the process
        process.add_pointer(new_pointer)
        for i in range(0,num_pages):
            self.page_id_generator += 1
            frame_address = self.allocate_page()
            if frame_address is None:
                memory_segment = self.replace_page()
                new_page = Page(memory_segment,self.page_id_generator)
            else:
                self.current_memory_usage += self.PAGE_SIZE
                new_page = Page(frame_address,self.page_id_generator)
            self.pointer_page_map[self.pointer_id_generator].append(new_page)
            self.fifo_queue.append(new_page)
    
    def process_use_command(self, pointer_id):
        if self.is_pointer_in_map(pointer_id):
            pages = self.pointer_page_map[pointer_id]
            for page in pages:
                if not page.in_ram:
                    frame_address = self.allocate_page()
                    if frame_address is None:
                        page.set_segment(self.replace_page())
                    else:
                        page.set_segment(frame_address)
                        self.current_memory_usage += self.PAGE_SIZE
                    page.set_in_ram()
                    self.fifo_queue.append(page)
        else:
            raise Exception("Couldn't find pointer")


    def process_delete_command(self,pointer_id):
        if self.is_pointer_in_map(pointer_id):
            pages = self.pointer_page_map[pointer_id]
            for page in pages:
                self.delete_pages_from_queue(page)
            del self.pointer_page_map[pointer_id]
        else:
            raise Exception("Couldn't find pointer")

    def process_kill_command(self,pid):
        process = self.get_process_by_pid(pid)
        self.processes.remove(process)
        pointers = process.get_pointers()
        for pointer in pointers:
            self.process_delete_command(pointer.get_pointer_id())

    def is_pointer_in_map(self,pointer_id):
        return pointer_id in self.pointer_page_map

    def get_process_by_pid(self,pid):
        for proc in self.processes:
            if proc.get_process_id() == pid:
                return proc
        raise Exception("Couldn't find process")

    #no se si hay que usar esto, porque la cosa es que si borro estas paginas directamente
    #Entonces se me van a borrar ciertos segmentos de memoria y se van a perder las direcciones
    def delete_pages_from_queue(self,page):
        for i in self.fifo_queue:
            if i.get_page_id() == page.get_page_id():
                self.available_addresses.append(page.get_segment())
                self.fifo_queue.remove(i)
                self.current_memory_usage -= self.PAGE_SIZE

    
    def get_process_by_pointer(self, pointer_id):
        for proc in self.processes:
            if proc.is_pointer_process(pointer_id):
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
        print("Map")
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
        print("Queue")
        for i in self.fifo_queue:
            i.print_page()

    def print_available_addresses(self):
        print("Available addresses")
        print(self.available_addresses)

    def print_memory_ussage(self):
        print("Memory usage")
        print(self.current_memory_usage)