import math
from Process import Process
from Pointer import Pointer
from Page import Page

class MMUOptimal():
    def __init__(self):
        self.pointer_references = []
        #It should be 400, 40 for testing purposes
        self.RAM = 400
        self.PAGE_SIZE  = 4
        self.FRAME_NUM = self.RAM // 4
        self.available_addresses = [i * self.PAGE_SIZE for i in range(self.FRAME_NUM)]
        self.current_memory_usage = 0
        self.current_v_memory_usage = 0
        self.pointer_id_generator = 0
        self.page_id_generator = 0
        self.pointer_page_map = {}
        self.processes = []
        self.loaded_pages = []
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
        for _ in range(0,num_pages):
            self.page_id_generator += 1
            frame_address = self.allocate_page()
            new_page = Page(frame_address,self.page_id_generator,self.current_v_memory_usage)
            new_page.set_associated_pointer(self.pointer_id_generator)
            self.current_memory_usage += self.PAGE_SIZE
            self.current_v_memory_usage += self.PAGE_SIZE
            self.pointer_page_map[self.pointer_id_generator].append(new_page)         
            self.loaded_pages.append(new_page)

    def increase_available_addresses(self, num_pages):
        for _ in range(0,num_pages):
            self.available_addresses.append(self.replace_page())

    def process_use_command(self,pointer_id):
        if not self.is_pointer_in_map(pointer_id):
            raise Exception("Couldn't find pointer when using",pointer_id)
        if self.pointer_references:
            self.pointer_references.remove(pointer_id)
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
                self.loaded_pages.append(page)
                #Aumentar el contador en 5s porque no estaba en ram
                self.clock += 5
                self.paging_clock += 5
            else:
                #Aumentar el reloj en 1s porque si estaba en ram
                self.clock += 1        

    def process_delete_command(self,pointer_id):
        if self.is_pointer_in_map(pointer_id):
            pages = self.pointer_page_map[pointer_id]
            for page in pages:
                self.delete_pages_from_loaded(page)
            del self.pointer_page_map[pointer_id]
            process = self.get_process_by_pointer(pointer_id)
            process.delete_pointer(pointer_id)
            self.delete_pointer_references(pointer_id)
        else:
            raise Exception("Couldn't find pointer when deleting", pointer_id)
        
    def delete_pointer_references(self, pointer_id):
        self.pointer_references = [x for x in self.pointer_references if x != pointer_id]
        
    def delete_pages_from_loaded(self,page):
        for i in self.loaded_pages:
            if i.get_page_id() == page.get_page_id():
                self.available_addresses.append(page.get_segment())
                self.loaded_pages.remove(page)
                self.current_memory_usage -= self.PAGE_SIZE

    def process_kill_command(self,pid):
        process = self.get_process_by_pid(pid)
        pointers = process.get_pointers()
        for pointer in pointers:
            self.process_delete_command(pointer.get_pointer_id())
        self.processes.remove(process)

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
        raise Exception("Coudln't find pointer when getting process by pointer", pointer_id)
    
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
        max_distance = - 1
        selected_page = None
        for page in self.loaded_pages:
            distance = self.get_page_distance(page)
            if distance > max_distance:
                max_distance = distance
                selected_page = page
            elif not distance:
                self.loaded_pages.remove(page)
                page.set_in_ram()
                return page.get_segment()
        self.loaded_pages.remove(selected_page)
        selected_page.set_in_ram()
        return selected_page.get_segment()

        

        
    def get_page_distance(self,page):
        try:
            self.pointer_references.index(page.get_associated_pointer())
        except ValueError:
            return False

    #You can use this to debug
    def print_map(self):
        print("Map")
        for k, v in self.pointer_page_map.items():
            print("Pointer key: ", k)
            for val in v:
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

    def get_ram_in_kb(self):
        return self.RAM - len(self.available_addresses)*self.PAGE_SIZE
    
    def get_ram_in_percentage(self):
        return (self.get_ram_in_kb()/self.RAM) * 100
    
    def get_vram_in_kb(self):
        vram_kb = 0
        for pointer in self.pointer_page_map:
            pages_in_vram = [x for x in self.pointer_page_map[pointer] if not x.in_ram]
            vram_kb += len(pages_in_vram) * self.PAGE_SIZE
        return vram_kb
    
    def get_vram_in_percentage(self):
        return ((self.get_vram_in_kb()+self.get_ram_in_kb())/self.RAM) * 100
    

    def get_trashing_time(self):
        return self.paging_clock
    
    def get_trashing_time_percentage(self):
        return (self.paging_clock / self.clock) * 100
    
    def get_fragmentation(self):
        return len(self.available_addresses) * self.PAGE_SIZE
    
    def get_total_time(self):
        return self.clock