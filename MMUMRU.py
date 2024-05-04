import math
from Process import Process
from Pointer import Pointer
from Page import Page
class MMUMRU():
    def __init__(self):
        #This is in kb
        #It should be 400, 40 for testing purposes
        self.RAM = 400
        self.PAGE_SIZE  = 4
        self.FRAME_NUM = self.RAM // 4
        self.available_addresses = [i * self.PAGE_SIZE for i in range(self.FRAME_NUM)]
        self.current_memory_usage = 0
        self.pointer_id_generator = 0
        self.page_id_generator = 0
        self.pointer_page_map = {}
        self.processes = []
        #Used to track overall time
        self.clock = 0
        #Used to track paging trashing time
        self.paging_clock = 0
        
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
        #If there are not enough addresses
        if len(self.available_addresses) < num_pages:
            #Number of pages that need room
            need_to_replace_number = num_pages - len(self.available_addresses)
            #Number of pages for which the address pool has room
            no_need_to_replace_number = len(self.available_addresses)
            self.increase_available_addresses(need_to_replace_number)
            #Increments both clock and paging clock by 5 seconds for each page that needed to be replaced
            self.clock += 5*need_to_replace_number
            self.paging_clock += 5*need_to_replace_number
            #Increments the clock by 1 second for each page that did not need to be replaced
            self.clock += 1*no_need_to_replace_number
        else:
            self.clock += 1*num_pages 
        for _ in range(0,num_pages):
            self.page_id_generator += 1
            frame_address = self.allocate_page()
            new_page = Page(frame_address,self.page_id_generator)
            self.current_memory_usage += self.PAGE_SIZE
            self.pointer_page_map[self.pointer_id_generator].append(new_page)
            #Change it to implement MRU
            self.fifo_queue.append(new_page)

    def process_use_command(self,pointer_id):
        if not self.is_pointer_in_map(pointer_id):
            raise Exception("Couldn't find pointer")   
        num_pages_of_pointer = len(self.pointer_page_map[pointer_id])
        if len(self.available_addresses) < num_pages_of_pointer:
            self.increase_available_addresses(num_pages_of_pointer)
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

    def process_delete_command(self,pointer_id):
        pass

    def process_kill_command(self,pid):
        pass

    def increase_available_addresses(self, num_pages):
        for _ in range(0,num_pages):
            page = self.mru_queue.pop(0)
            page.set_in_ram()
            self.available_addresses.append(page.get_segment())

    def is_pointer_in_map(self,pointer_id):
        return pointer_id in self.pointer_page_map
