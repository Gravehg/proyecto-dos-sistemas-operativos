#from tkinter import *
#from tkinter import ttk 
#root = Tk()
#ttk.Button(root,text="Hello World").grid()
#root.mainloop()
from MMUFIFO import MMUFIFO

new_mmu = MMUFIFO()
#new_mmu.print_something()
new_mmu.process_new_command(1,12500)
new_mmu.process_new_command(1,25000)
new_mmu.process_new_command(2,25000)
new_mmu.print_processes_pointers()