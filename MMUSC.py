from Process import Process  
from Pointer import Pointer  
from Page import Page  
from queue import Queue  
import math  

class MMUSecondChance():
    def __init__(self):
        self.RAM = 400  # Tamaño de la RAM en KB
        self.PAGE_SIZE = 4  # Tamaño de página en KB
        self.current_memory = 0  # Memoria actualmente en uso
        self.pointer_id_generator = 0  # Generador de IDs para punteros
        self.page_id_generator = 0  # Generador de IDs para páginas
        self.pointer_page_map = {}  # Mapa que relaciona punteros con páginas
        self.processes = []  # Lista de procesos
        self.second_chance_queue = Queue()  # Cola para el algoritmo de segunda oportunidad

    # Método para procesar el comando 'new' y asignar memoria a un proceso nuevo
    def process_new_command(self, pid, size):
        kb_size = size / 1000  # Convertir el tamaño de bytes a KB
        num_pages = math.ceil(kb_size / 4)  # Calcular el número de páginas necesarias
        process = self.get_process(pid)  # Obtener el proceso existente o crear uno nuevo
        new_pointer = self.create_pointer()  # Crear un nuevo puntero para el proceso
        process.add_pointer(new_pointer)  # Agregar el puntero al proceso
        for i in range(num_pages):
            # Crear y asignar páginas al puntero del proceso
            memory_required = 4  # Tamaño de memoria requerido por la página
            if self.current_memory + memory_required > self.RAM:
                self.replace_page()  # Reemplazar una página si la memoria está llena
            self.page_id_generator += 1  # Generar un nuevo ID de página
            new_page = Page(self.page_id_generator)  # Crear una nueva página
            new_pointer.add_page(new_page)  # Agregar la página al puntero
            self.second_chance_queue.put(new_page)  # Agregar la página a la cola de segunda oportunidad

    def process_use_command(self, pointer_id):
        # Método para procesar el comando 'use' y permitir que un proceso use un puntero
        process = self.get_process_by_pointer(pointer_id)  # Obtener el proceso que posee el puntero
        pointer = process.get_pointer(pointer_id)  # Obtener el puntero del proceso
        if pointer:
            # Realizar acciones adicionales según sea necesario
            print(f"El proceso {process.get_process_id()} está usando el puntero {pointer_id}.")
        else:
            print("El puntero especificado no existe en la tabla de símbolos del proceso.")

    def process_delete_command(self, pointer_id):
        # Método para procesar el comando 'delete' y eliminar un puntero de un proceso
        process = self.get_process_by_pointer(pointer_id)  # Obtener el proceso que posee el puntero
        pointer = process.get_pointer(pointer_id)  # Obtener el puntero del proceso
        if pointer:
            # Eliminar el puntero del proceso
            process.remove_pointer(pointer_id)
            # Liberar la memoria asociada al puntero eliminado
            for page in pointer.get_pages():
                self.release_page(page)
            print(f"El puntero {pointer_id} ha sido eliminado del proceso {process.get_process_id()}.")
        else:
            print("El puntero especificado no existe en la tabla de símbolos del proceso.")


    def replace_page(self):
        # Método para reemplazar una página en la RAM utilizando el algoritmo de segunda oportunidad
        while not self.second_chance_queue.empty():
            page = self.second_chance_queue.get()  # Obtener una página de la cola
            if page.has_reference():
                # Dar a la página una segunda oportunidad si tiene referencia
                page.clear_reference()
                self.second_chance_queue.put(page)  # Devolver la página a la cola
            else:
                # Reemplazar la página si no tiene referencia
                page_id_to_remove = page.get_page_id()  # Obtener el ID de la página a eliminar
                for pointer_id, pages in self.pointer_page_map.items():
                    for p in pages:
                        if p.get_page_id() == page_id_to_remove:
                            # Eliminar la página del mapa de punteros y actualizar la memoria
                            self.pointer_page_map[pointer_id].remove(p)
                            self.current_memory -= self.PAGE_SIZE
                            break
                page.set_in_ram()  # Marcar la nueva página como en la RAM
                return  # Salir del bucle después de reemplazar una página




    def print_map(self):
        for pages in self.pointer_page_map.values():
            for page in pages:
                page.print_page()

    def print_processes_pointers(self):
        for proc in self.processes:
            print("Process ID is:", proc.get_process_id())
            proc.print_pointers()
            print("-------------------------------------")
