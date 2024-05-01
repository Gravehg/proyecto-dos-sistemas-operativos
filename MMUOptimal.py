class MMUOptimal():
    def __init__(self):
        self.pointer_references = []
        #It should be 400, 40 for testing purposes
        self.RAM = 400
        self.PAGE_SIZE  = 4
        self.FRAME_NUM = self.RAM // 4
        self.available_addresses = [i * self.PAGE_SIZE for i in range(self.FRAME_NUM)]
        self.current_memory_usage = 0
        self.pointer_id_generator = 0
        self.page_id_generator = 0
        self.pointer_page_map = {}
        self.processes = []
        self.fifo_queue = []
        #Used to track overall time
        self.clock = 0
        #Used to track paging trashing time
        self.paging_clock = 0

    
    def process_new_command(self,pid,size):
        pass

    def process_use_command(self,pointer_id):
        pass

    def process_delete_command(self,pointer_id):
        pass

    def process_kill_command(self,pid):
        pass