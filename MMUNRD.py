import random
import math
from Process import Process
from Pointer import Pointer
from Page import Page

class MMURND():
    def __init__(self):
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
        self.clock = 0
        self.paging_clock = 0
        self.wasted_thrashing_space = 0

    def allocate_page(self):
        if not self.available_addresses:
            return None  # No available pages left
        return self.available_addresses.pop(0)

    def process_new_command(self, pid, size):
        kb_size = size / 1000
        exact_num_pages = kb_size / 4
        num_pages = math.ceil(exact_num_pages)
        exact_space_required = exact_num_pages * self.PAGE_SIZE
        rounded_space_required = num_pages * self.PAGE_SIZE
        self.wasted_thrashing_space += rounded_space_required - exact_space_required
        new_solicitude_wasted_space = rounded_space_required - exact_space_required
        process = None
        if self.is_existing_process(pid):
            process = self.get_process(pid)
        else:
            process = self.create_process(pid)
        new_pointer = self.create_pointer(new_solicitude_wasted_space)
        process.add_pointer(new_pointer)
        if len(self.available_addresses) < num_pages:
            need_to_replace_number = num_pages - len(self.available_addresses)
            no_need_to_replace_number = len(self.available_addresses)
            self.current_memory_usage += self.PAGE_SIZE * no_need_to_replace_number
            self.increase_available_addresses(need_to_replace_number)
            self.clock += 5*need_to_replace_number
            self.paging_clock += 5*need_to_replace_number
            self.clock += 1*no_need_to_replace_number
        else:
            self.clock += 1*num_pages 
            self.current_memory_usage += self.PAGE_SIZE * num_pages
        for _ in range(0,num_pages):
            self.page_id_generator += 1
            memory_segment = self.allocate_page()
            new_page = Page(memory_segment,self.page_id_generator, self.current_v_memory_usage)
            self.current_v_memory_usage += self.PAGE_SIZE
            self.pointer_page_map[self.pointer_id_generator].append(new_page)
            self.loaded_pages.append(new_page)
    
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
            self.loaded_pages.append(page)
            self.clock += 5
            self.paging_clock += 5
            pages_in_ram.append(page)
        self.clock += 1*time_pages_in_ram


    def replace_page_use(self, do_not_replace_pages):
            replaceable = False
            page = None
            while not replaceable:
                random_page_index = random.randint(0, len(self.loaded_pages) - 1)
                if not self.loaded_pages[random_page_index] in do_not_replace_pages:
                    page = self.loaded_pages.pop(random_page_index)
                    page.set_in_ram()
                    replaceable = True
            return page.get_segment()

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

    def process_kill_command(self, pid):
        process = self.get_process_by_pid(pid)
        pointers = process.get_pointers()
        for pointer in pointers:
            self.process_delete_command(pointer.get_pointer_id())
        self.processes.remove(process)

    def is_pointer_in_map(self, pointer_id):
        return pointer_id in self.pointer_page_map

    def get_process_by_pid(self, pid):
        for proc in self.processes:
            if proc.get_process_id() == pid:
                return proc
        raise Exception("Couldn't find process")

    def delete_pages_from_queue(self, page):
        for i in self.loaded_pages:
            if i.get_page_id() == page.get_page_id():
                self.available_addresses.append(page.get_segment())
                self.loaded_pages.remove(page)
                self.current_memory_usage -= self.PAGE_SIZE

    def get_process_by_pointer(self, pointer_id):
        for proc in self.processes:
            if proc.is_pointer_process(pointer_id):
                return proc
        raise Exception("Couldn't find pointer when getting process by pointer", pointer_id)

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
        if self.loaded_pages:
            random_page_index = random.randint(0, len(self.loaded_pages) - 1)
            page = self.loaded_pages.pop(random_page_index)
            page.set_in_ram()
            return page.get_segment()

    def print_map(self):
        print("Map")
        for k, v in self.pointer_page_map.items():
            print("Pointer key: ", k)
            for val in v:
                val.print_page()

    def print_processes_pointers(self):
        for proc in self.processes:
            print("Process ID is: ", proc.get_process_id())
            proc.print_pointers()
            print("-------------------------------------")

    def print_queue(self):
        print("Queue")
        for i in self.loaded_pages:
            i.print_page()

    def print_available_addresses(self):
        print("Available addresses")
        print(self.available_addresses)

    def print_memory_ussage(self):
        print("Memory usage")
        print(self.current_memory_usage)

    def get_ram_in_kb(self):
        return self.RAM - len(self.available_addresses) * self.PAGE_SIZE
    
    def get_ram_in_percentage(self):
        return (self.get_ram_in_kb() / self.RAM) * 100
    
    def get_vram_in_kb(self):
        vram_kb = 0
        for pointer in self.pointer_page_map:
            pages_in_vram = [x for x in self.pointer_page_map[pointer] if not x.in_ram]
            vram_kb += len(pages_in_vram) * self.PAGE_SIZE
        return vram_kb
    
    def get_vram_in_percentage(self):
        return ((self.get_vram_in_kb() + self.get_ram_in_kb()) / self.RAM) * 100

    def get_trashing_time(self):
        return self.paging_clock
    
    def get_trashing_time_percentage(self):
        return (self.paging_clock / self.clock) * 100
    
    def get_fragmentation(self):
        return self.wasted_thrashing_space
    
    def get_total_time(self):
        return self.clock
