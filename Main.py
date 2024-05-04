#from tkinter import *
#from tkinter import ttk 
#root = Tk()
#ttk.Button(root,text="Hello World").grid()
#root.mainloop()
from MMUFIFO import MMUFIFO
from FileProcessor import FileProcessor
from FileGenerator import FileGenerator
import time

new_file_generator = FileGenerator(10,5000,1282817)
new_file_generator.generate_file()
new_file_processor = FileProcessor("test.txt", "FIFO")
while(new_file_processor.instruction_list):
    #time.sleep(1)
    new_file_processor.process_instruction()
    print("Selected clock" ,new_file_processor.selected_mmu.clock)
    print("Optimal clock", new_file_processor.optimal_mmu.clock)
