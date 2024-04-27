#from tkinter import *
#from tkinter import ttk 
#root = Tk()
#ttk.Button(root,text="Hello World").grid()
#root.mainloop()
from MMUFIFO import MMUFIFO
from FileProcessor import FileProcessor

new_mmu = MMUFIFO()
new_file_processor = FileProcessor()
new_file_processor.process_file('test.txt')
#new_mmu.print_something()
new_mmu.process_new_command(1,40000)
print("Map:")
new_mmu.print_map()
print()
print("Queue")
new_mmu.print_queue()
new_mmu.process_new_command(1,25000)
print("Map")
new_mmu.print_map()
print()
print("Queue")
new_mmu.print_queue()
new_mmu.process_new_command(2,25000)
new_mmu.print_processes_pointers()