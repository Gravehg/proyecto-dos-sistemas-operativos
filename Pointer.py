class Pointer():
    def __init__(self, id, fragmentation):
        self.id = id
        self.fragmentation = fragmentation
    
    def get_pointer_id(self):
        return self.id
    
    def get_pointer_fragmentation(self):
        return self.fragmentation