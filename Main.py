#from tkinter import *
#from tkinter import ttk 
#root = Tk()
#ttk.Button(root,text="Hello World").grid()
#root.mainloop()
from MMUFIFO import MMUFIFO
from FileProcessor import FileProcessor
from FileGenerator import FileGenerator
import time

new_mmu = MMUFIFO()
#new_file_processor = FileProcessor("ask","pbt")
#new_file_processor.read_file_instructions('test.txt')
#new_mmu.print_something()
new_mmu.print_available_addresses()
new_mmu.process_new_command(1,40000)
new_mmu.print_memory_ussage()
new_mmu.print_available_addresses()
new_mmu.process_new_command(1,25000)
new_mmu.print_memory_ussage()
new_mmu.print_map()
new_mmu.print_queue()
new_mmu.process_new_command(2,25000)
new_mmu.process_new_command(2,25000)
new_mmu.print_map()
new_mmu.print_queue()
#new_mmu.process_use_command(1)
new_mmu.process_use_command(2)
new_mmu.print_map()
new_mmu.print_queue()
#new_mmu.process_kill_command(1)
new_mmu.print_map()
new_mmu.print_queue()
new_mmu.print_available_addresses()
new_mmu.process_delete_command(3)
new_mmu.process_delete_command(4)
new_mmu.print_memory_ussage()
new_mmu.print_memory_ussage()
print(new_mmu.get_ram_in_kb())
print(new_mmu.get_ram_in_percentage())
print(new_mmu.get_vram_in_kb())
print(new_mmu.get_vram_in_percentage())
print(new_mmu.clock)
print(new_mmu.get_trashing_time())
print(new_mmu.get_trashing_time_percentage())
new_file_generator = FileGenerator(10,5000,1282817)
new_file_generator.generate_file()
new_file_processor = FileProcessor("test.txt", "SC")
while(new_file_processor.instruction_list):
    #time.sleep(1)
    new_file_processor.process_instruction()
    print("Selected clock" ,new_file_processor.selected_mmu.clock)
    print("Optimal clock", new_file_processor.optimal_mmu.clock)
