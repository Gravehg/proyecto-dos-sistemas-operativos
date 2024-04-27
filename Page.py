class Page():
    def __init__(self, segment, page_id):
        self.id = page_id
        self.segment = segment
        self.in_ram = True
    
    def set_in_ram(self):
        self.in_ram = not self.in_ram

    def get_segment(self):
        return self.segment

    def print_page(self):
        print(self.id, self.segment, self.in_ram)