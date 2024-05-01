class Page():
    def __init__(self, segment, page_id):
        self.id = page_id
        self.segment = segment
        self.in_ram = True
        self.bit = False
    
    def set_in_ram(self):
        self.in_ram = not self.in_ram

    def set_segment(self,segment):
        self.segment = segment

    def get_segment(self):
        return self.segment
    
    def get_page_id(self):
        return self.id

    def in_ram(self):
        return self.in_ram

    def print_page(self):
        print(self.id, self.segment, self.in_ram)

    def set_bit(self):
        self.bit = not self.bit