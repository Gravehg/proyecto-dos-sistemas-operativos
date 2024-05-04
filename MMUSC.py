from Process import Process  
from Pointer import Pointer  
from Page import Page  
#from queue import Queue  
import math  

class MMUSecondChance():
    def __init__(self):
        self.RAM = 400  # Tamaño de la RAM en KB
        self.PAGE_SIZE = 4  # Tamaño de página en KB
        self.FRAME_NUM = self.RAM // 4
        self.available_addresses = [i * self.PAGE_SIZE for i in range(self.FRAME_NUM)]
        self.current_memory_usage = 0  # Memoria actualmente en uso
        self.current_v_memory_usage = 0
        self.pointer_id_generator = 0  # Generador de IDs para punteros
        self.page_id_generator = 0  # Generador de IDs para páginas
        self.pointer_page_map = {}  # Mapa que relaciona punteros con páginas
        self.processes = []  # Lista de procesos
        self.second_chance_queue = []  # Cola para el algoritmo de segunda oportunidad
        #Used to track overall time
        self.clock = 0
        #Used to track paging trashing time
        self.paging_clock = 0

    def allocate_page(self):
        if not self.available_addresses:
            return None  # No available pages left
        return self.available_addresses.pop(0)

    # Método para procesar el comando 'new' y asignar memoria a un proceso nuevo
    def process_new_command(self, pid, size):
        kb_size = size / 1000  # Convertir el tamaño de bytes a KB
        num_pages = math.ceil(kb_size / 4)  # Calcular el número de páginas necesarias
        process = self.get_process(pid)  # Obtener el proceso existente o crear uno nuevo
        new_pointer = self.create_pointer()  # Crear un nuevo puntero para el proceso
        process.add_pointer(new_pointer)  # Agregar el puntero al proceso
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
            self.second_chance_queue.append(new_page)

    def increase_available_addresses(self, num_pages):
        for _ in range(0,num_pages):
            self.available_addresses.append(self.replace_page())

    def process_use_command(self, pointer_id):
        if not self.is_pointer_in_map(pointer_id):
            raise Exception("Couldn't find pointer")
        pages = self.pointer_page_map[pointer_id]
        #Setear el bit en ambos casos, porque se hace la referencia tanto si esta como si no esta en RAM
        for page in pages:
            if not page.in_ram:
                frame_address = self.allocate_page()
                if frame_address is None:
                    page.set_segment(self.replace_page())
                else:
                    page.set_segment(frame_address)
                    self.current_memory_usage += self.PAGE_SIZE
                page.set_in_ram()
                page.set_bit()
                self.second_chance_queue.append(page)
                #Aumentar el contador en 5s porque no estaba en ram
                self.clock += 5
                self.paging_clock += 5
            else:
                page.set_bit()
                #Aumentar el reloj en 1s porque si estaba en ram
                self.clock += 1

    def process_delete_command(self, pointer_id):
        if self.is_pointer_in_map(pointer_id):
            pages = self.pointer_page_map[pointer_id]
            for page in pages:
                self.delete_pages_from_queue(page)
            del self.pointer_page_map[pointer_id]
            process = self.get_process_by_pointer(pointer_id)
            process.delete_pointer(pointer_id)
        else:
            raise Exception("Couldn't find pointer")
        
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
        for i in self.second_chance_queue:
            if i.get_page_id() == page.get_page_id():
                self.available_addresses.append(page.get_segment())
                self.second_chance_queue.remove(page)
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
        replaced = False
        p = None
        while(not replaced):
            if self.second_chance_queue[0].bit:
                p = self.second_chance_queue.pop(0)
                p.set_bit()
                self.second_chance_queue.append(p)
            else:
                p = self.second_chance_queue.pop(0)
                replaced = True
        return p.get_segment()
              
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
        for i in self.second_chance_queue_queue:
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
