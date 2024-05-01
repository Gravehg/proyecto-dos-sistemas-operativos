import math
import random  # Importamos el módulo random para generar números aleatorios
from Process import Process
from Pointer import Pointer
from Page import Page
from queue import Queue

class MMURND():
    def __init__(self):
        self.RAM = 400
        self.PAGE_SIZE = 4
        self.current_memory = 0
        self.pointer_id_generator = 0
        self.page_id_generator = 0
        self.pointer_page_map = {}
        self.processes = []
        self.rnd_queue = []  # Utilizamos una lista en lugar de una cola para el algoritmo RND

    def process_new_command(self, pid, size):
        kb_size = size / 1000
        num_pages = math.ceil(kb_size / 4)
        process = self.get_process(pid)
        new_pointer = self.create_pointer()
        process.add_pointer(new_pointer)
        for i in range(num_pages):
            memory_required = 4

            if self.current_memory + memory_required > self.RAM:
                self.replace_page()

            self.page_id_generator += 1
            new_page = Page(self.page_id_generator)
            new_pointer.add_page(new_page)
            self.rnd_queue.append(new_page)  # Agregamos la página a la lista para el algoritmo RND

    def process_use_command(self, pointer_id):
        process = self.get_process_by_pointer(pointer_id)
        pointer = process.get_pointer(pointer_id)
        if pointer:
            # Realizar acciones adicionales según sea necesario
            print(f"El proceso {process.get_process_id()} está usando el puntero {pointer_id}.")
        else:
            print("El puntero especificado no existe en la tabla de símbolos del proceso.")

    def process_delete_command(self, pointer_id):
        process = self.get_process_by_pointer(pointer_id)
        pointer = process.get_pointer(pointer_id)
        if pointer:
            process.remove_pointer(pointer_id)
            for page in pointer.get_pages():
                # Liberar memoria asociada al puntero eliminado
                self.release_page(page)
            print(f"El puntero {pointer_id} ha sido eliminado del proceso {process.get_process_id()}.")
        else:
            print("El puntero especificado no existe en la tabla de símbolos del proceso.")
            
    def get_process_by_pointer(self, pointer_id):
        for proc in self.processes:
            if proc.is_pointer_process(pointer_id):
                return proc
        raise Exception("Couldn't find pointer")

    def get_process(self, pid):
        for proc in self.processes:
            if proc.get_process_id() == pid:
                return proc
        process = Process(pid)
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
        if self.rnd_queue:  # Verificamos si la lista no está vacía antes de reemplazar la página
            page_to_replace = random.choice(self.rnd_queue)  # Seleccionamos una página aleatoria de la lista
            self.rnd_queue.remove(page_to_replace)  # Eliminamos la página seleccionada de la lista
            page_id_to_remove = page_to_replace.get_page_id()
            for pointer_id, pages in self.pointer_page_map.items():
                for p in pages:
                    if p.get_page_id() == page_id_to_remove:
                        self.pointer_page_map[pointer_id].remove(p)
                        self.current_memory -= self.PAGE_SIZE
                        break
            page_to_replace.set_in_ram()  # Marcamos la nueva página como en la RAM

    def print_map(self):
        for pages in self.pointer_page_map.values():
            for page in pages:
                page.print_page()

    def print_processes_pointers(self):
        for proc in self.processes:
            print("Process ID is:", proc.get_process_id())
            proc.print_pointers()
            print("-------------------------------------")
