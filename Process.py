class Process():
    def __init__(self, id):
        self.id = id
        self.pointers = []
        
    def add_pointer(self,pointer):
        self.pointers.append(pointer)

    def get_process_id(self):
        return self.id

    def get_pointers(self):
        return self.pointers

    def is_pointer_process(self, pointer_id):
        for pointer in self.pointers:
            if pointer.get_pointer_id() == pointer_id:
                return True
        return False

    def delete_pointer(self,pointer_id):
        for pointer in self.pointers:
            if pointer.get_pointer_id() == pointer_id:
                self.pointers.remove(pointer)

    def print_pointers(self):
        for pointer in self.pointers:
            print("Pointer id is: ", pointer.get_pointer_id())

    def get_pointer_fragmentation(self, pointer_id):
        for pointer in self.pointers:
            if pointer.get_pointer_id() == pointer_id:
                return pointer.get_pointer_fragmentation()
            
    def get_pointers_list(self):
        list_pointers = []
        
        for pointer in self.pointers:
            list_pointers.append(pointer.get_pointer_id())
            
        return list_pointers
