import math
from Process import Process
from Pointer import Pointer
from Page import Page
#from queue import Queue


class MMUFIFO():
    def __init__(self):
        #This is in kb
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
        self.fifo_queue = []
        #Used to track overall time
        self.clock = 0
        #Used to track paging trashing time
        self.paging_clock = 0
        self.wasted_thrashing_space = 0 
    
    def allocate_page(self):
        if not self.available_addresses:
            return None  # No available pages left
        return self.available_addresses.pop(0)

    def process_new_command(self,pid,size):
        kb_size = size / 1000
        exact_num_pages = kb_size / 4
        num_pages = math.ceil(exact_num_pages)
        exact_space_required = exact_num_pages * self.PAGE_SIZE
        rounded_space_required = num_pages * self.PAGE_SIZE
        self.wasted_thrashing_space += rounded_space_required - exact_space_required
        #Gets the process if it already exists, if not, then returns a new one
        new_solicitude_wasted_space = rounded_space_required - exact_space_required
        process = None
        if self.is_existing_process(pid):
            process = self.get_process(pid)
        else:
            process = self.create_process(pid)
        #Creates the new pointer
        new_pointer = self.create_pointer(new_solicitude_wasted_space)
        #Adds the pointer to the list of the process
        process.add_pointer(new_pointer)
        #Si hay que reemplazar paginas
        if len(self.available_addresses) < num_pages:
            #Number of pages that need room
            need_to_replace_number = num_pages - len(self.available_addresses)
            #Number of pages for which the address pool has room
            no_need_to_replace_number = len(self.available_addresses)
            #Suma la cantidad de paginas que son NUEVAS EN LA RAM
            self.current_memory_usage += self.PAGE_SIZE * no_need_to_replace_number
            #Evicts the number of pages that need replacement
            self.increase_available_addresses(need_to_replace_number)
            #Increments both clock and paging clock by 5 seconds for each page that needed to be replaced
            self.clock += 5*need_to_replace_number
            self.paging_clock += 5*need_to_replace_number
            #Increments the clock by 1 second for each page that did not need to be replaced
            self.clock += 1*no_need_to_replace_number
        else:
            #If there is room for all pages, then just adds 1 second for each page
            self.clock += 1*num_pages 
            self.current_memory_usage += self.PAGE_SIZE * num_pages
        for _ in range(0,num_pages):
            self.page_id_generator += 1
            memory_segment = self.allocate_page()
            new_page = Page(memory_segment,self.page_id_generator, self.current_v_memory_usage)
            self.current_v_memory_usage += self.PAGE_SIZE
            self.pointer_page_map[self.pointer_id_generator].append(new_page)
            self.fifo_queue.append(new_page)
    
    def process_use_command(self, pointer_id):
        if not self.is_pointer_in_map(pointer_id):
            raise Exception("Couldn't find pointer when using",pointer_id)
        pages = self.pointer_page_map[pointer_id]
        pages_in_ram = [p for p in pages if p.in_ram]
        time_pages_in_ram = len(pages_in_ram);
        pages_not_in_ram = [p for p in pages if not p.in_ram]
        for page in pages_not_in_ram:
            frame_address = self.allocate_page()
            if frame_address is None:
                page.set_segment(self.replace_page_use(pages_in_ram))
            else:
                page.set_segment(frame_address)
                self.current_memory_usage += self.PAGE_SIZE
            page.set_in_ram()
            self.fifo_queue.append(page)
                #Aumentar el contador en 5s porque no estaba en ram
            self.clock += 5
            self.paging_clock += 5
            pages_in_ram.append(page)
        self.clock += 1*time_pages_in_ram

    def replace_page_use(self,do_not_replace_pages):
        if not len(self.fifo_queue) == 0:
            selected_page = None
            found = False
            for p in self.fifo_queue:
                for dnp in do_not_replace_pages:
                    if p.get_page_id() != dnp.get_page_id():
                        found = True
                        break
                if found:
                    selected_page = p
                    break
            selected_page.set_in_ram()
            self.fifo_queue.remove(selected_page)
            return selected_page.get_segment()

            
    def process_delete_command(self,pointer_id):
        if self.is_pointer_in_map(pointer_id):
            pages = self.pointer_page_map[pointer_id]
            for page in pages:
                self.delete_pages_from_queue(page)
            del self.pointer_page_map[pointer_id]
            process = self.get_process_by_pointer(pointer_id)
            self.wasted_thrashing_space -= process.get_pointer_fragmentation(pointer_id)
            process.delete_pointer(pointer_id)
        else:
            raise Exception("Couldn't find pointer when deleting", pointer_id)

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
        if page in self.fifo_queue:
            self.available_addresses.append(page.get_segment())
            self.fifo_queue.remove(page)
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
        raise Exception("Used unexisting process")
    
    def create_process(self,id):
        process = Process(id)
        self.processes.append(process)
        return process
    
    def is_existing_process(self,pid):
        for proc in self.processes:
            if proc.get_process_id() == pid:
                return True
        return False 
    
    def create_pointer(self,new_solicitude_wasted_space):
        self.pointer_id_generator += 1
        new_pointer_id = self.pointer_id_generator 
        new_pointer = Pointer(new_pointer_id,new_solicitude_wasted_space)
        if self.pointer_id_generator not in self.pointer_page_map:
            self.pointer_page_map[self.pointer_id_generator] = []
        return new_pointer
    
    def increase_available_addresses(self, num_pages):
        for _ in range(0,num_pages):
            self.available_addresses.append(self.replace_page())

    def replace_page(self):
        if not len(self.fifo_queue) == 0:
            page = self.fifo_queue.pop(0)
            page.set_in_ram()
            return page.get_segment()

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
        return self.wasted_thrashing_space
    
    def get_total_time(self):
        return self.clock
    
    #-----------------------
    
    def get_num_process(self):
        len = 0
        for proc in self.processes:
            len += 1
        return len
    
    def get_process_map(self):
        process_map = {}
        for proc in self.processes:
            process_id = str(proc.get_process_id())
            list_pointers = proc.get_pointers_list()
            process_map[str(process_id)] = list_pointers 
        
        return process_map
    
    def get_pages_map(self):
        all_pointers = {}
        
        for k,v in self.pointer_page_map.items():
            pages_list = []
            
            for val in v:
                pages_list.append(val.get_all())
                
            all_pointers.setdefault(k,pages_list)
            
        return all_pointers
    
    def get_table_info(self):
        processes_map = self.get_process_map()
        pointers_map = self.get_pages_map()
        table_info = []
        
        for k,v in pointers_map.items():
            self.pid_pointer = None
            self.page_id = None
            self.loaded = None
            self.l_addr = None
            m_addr = None
            loaded_t = None
            mark = None
            
            for k1, v1 in processes_map.items():
                if k in v1:
                    self.pid_pointer = k1
            
            for vals in v:
                self.page_id = vals["id"]
                self.loaded = vals["in_ram"]
                if self.loaded:
                    table_info.append([str(self.page_id), str(self.pid_pointer), "X", "-", "-", "-", "-", "NO"])
                else:
                    table_info.append([str(self.page_id), str(self.pid_pointer), "", "-", "-", "-", "-", ""])
            
                        
            
        return table_info
    
    def get_color_ram_info(self):
        processes_map = self.get_process_map()
        pointers_map = self.get_pages_map()
        
        colors_info = {}
        
        for k,v in pointers_map.items():
            counter = 0
            self.id_process = None
            
            for k1,v1 in processes_map.items():
                if k in v1:
                    self.id_process = int(k1)
            
            for vals in v:
                counter += 1
            
            process_in_list = False
            for k2,v1 in colors_info.items():
                if self.id_process == int(k2):
                    process_in_list = True
            
            if process_in_list:
                valor = colors_info[self.id_process] + counter
                colors_info[self.id_process] = valor
            else:
                colors_info.setdefault(self.id_process,counter)
                
        return colors_info
    
    def get_pages_loaded_and_unloaded(self):
        pointers_map = self.get_pages_map()
        count_loaded = 0
        count_unloaded = 0
        
        for k, v in pointers_map.items():
            for val in v:
                if val["in_ram"] == True:
                    count_loaded += 1
                else:
                    count_unloaded +=1
                    
        return [count_loaded,count_unloaded]
            
        
        
        