import tkinter as tk
import customtkinter
import time
from FileProcessor import FileProcessor
from FileGenerator import FileGenerator
from tkinter.filedialog import askopenfile


#Window TkInter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
#window = customtkinter.CTk()

# Variables


#Statistics Change Variables



class main_proyect(customtkinter.CTk):  
    def __init__(self):
        super().__init__()
        self.file_processor = None
        self.file_generator = None
        self.selected_file = None
        self.name_file = tk.StringVar()
        self.name_algorithm = tk.StringVar()
        self.name_algorithm.set("RAM - [ALG]")
        self.name_mmu = tk.StringVar()
        self.name_mmu.set("MMU - [ALG]")
        
        self.processes_opt = tk.StringVar()
        self.sim_time_opt = tk.StringVar()
        self.ram_kb_opt = tk.StringVar()
        self.ram_percentage_opt = tk.StringVar()
        self.v_ram_kb_opt = tk.StringVar()
        self.v_ram_percentage_opt = tk.StringVar()
        self.loaded_pages_opt = tk.StringVar()
        self.unloaded_pages_opt = tk.StringVar()
        self.seconds_thrashing_opt = tk.StringVar()
        self.percentage_thrashing_opt = tk.StringVar()
        self.fragmentacion_opt = tk.StringVar()

        self.processes_alg = tk.StringVar()
        self.sim_time_alg = tk.StringVar()
        self.ram_kb_alg = tk.StringVar()
        self.ram_percentage_alg = tk.StringVar()
        self.v_ram_kb_alg = tk.StringVar()
        self.v_ram_percentage_alg = tk.StringVar()
        self.loaded_pages_alg = tk.StringVar()
        self.unloaded_pages_alg = tk.StringVar()
        self.seconds_thrashing_alg = tk.StringVar()
        self.percentage_thrashing_alg = tk.StringVar()
        self.fragmentacion_alg = tk.StringVar()

        self.processes_opt.set("-")
        self.sim_time_opt.set("-")
        self.ram_kb_opt.set("-")
        self.ram_percentage_opt.set("-")
        self.v_ram_kb_opt.set("-")
        self.v_ram_percentage_opt.set("-")
        self.loaded_pages_opt.set("-")
        self.unloaded_pages_opt.set("-")
        self.seconds_thrashing_opt.set("-")
        self.percentage_thrashing_opt.set("-")
        self.fragmentacion_opt.set("-")

        self.processes_alg.set("-")
        self.sim_time_alg.set("-")
        self.ram_kb_alg.set("-")
        self.ram_percentage_alg.set("-")
        self.v_ram_kb_alg.set("-")
        self.v_ram_percentage_alg.set("-")
        self.loaded_pages_alg.set("-")
        self.unloaded_pages_alg.set("-")
        self.seconds_thrashing_alg.set("-")
        self.percentage_thrashing_alg.set("-")
        self.fragmentacion_alg.set("-")

        self.list_MMU_OPT = [('PAGE ID', 'PID', 'LOADED', 'L-ADDR', 'M-ADDR', 'D-ADDR', 'LOADED-T', 'MARK'),
                ('1','1','X','1','1','-','0s','-', ("yellow", "black")),] 
        self.list_MMU_ALG = [('PAGE ID', 'PID', 'LOADED', 'L-ADDR', 'M-ADDR', 'D-ADDR', 'LOADED-T', 'MARK'),
                ('1','1','X','1','1','-','0s','-', ("yellow", "black")),]
        self.dic_MMU_OPT = {
            "processes":"5",
            "sim-time": "250s",
            "ram-kb": "244",
            "ram-percentage": "61",
            "v-ram-kb" : "40",
            "v-ram-percentage": "4%",
            "pages": {
                "loaded": "61",
                "unloaded": "85"
            },
            "thrashing": {
                "seconds": "150s",
                "percentage": "60%"
            },
            "fragmentacion": "256KB"
        }

        self.dic_MMU_ALG = {
            "processes":"5",
            "sim-time": "250s",
            "ram-kb": "244",
            "ram-percentage": "61",
            "v-ram-kb" : "40",
            "v-ram-percentage": "4%",
            "pages": {
                "loaded": "61",
                "unloaded": "85"
            },
            "thrashing": {
                "seconds": "150s",
                "percentage": "60%"
            },
            "fragmentacion": "256KB"
        }
        
        self.initial_configurations()
        self.init_tables()
        self.another_init()
        self.mainloop()
   
    def upload_file(self):
        self.selected_file = askopenfile(mode="r", filetypes=[('Archivos de texto', '*.txt')])
            
    def execute_program(self):
            if self.selected_file is not None:
                self.file_processor = FileProcessor(self.selected_file.name, self.configure_algorithm_combo.get())
                self.name_file.set(self.selected_file.name)
            else:
                seed = None
                if not self.configure_seed_entry.get():
                    seed = 1000
                else:
                    seed = int(self.configure_seed_entry.get())
                self.file_generator = FileGenerator(int(self.configure_process_combo.get()),int(self.configure_operations_combo.get()),seed)
                self.file_generator.generate_file()
                self.file_processor = FileProcessor(self.file_generator.file_name, self.configure_algorithm_combo.get())
                #Feeds page references to optimal MMU
                self.file_processor.feed_opt_references()

            #Un tipo wait o algo asi antes de ejecutar la siguiente instruction
            #While len(self.file_processor.instruction) > 0
            # self,file_processor.processes_instruction()
            # wait(algunos_segundos)
            #while self.file_processor.instruction_list:
                #self.file_processor.process_instruction()
                #time.sleep(1)
                #print(self.file_processor.selected_mmu.get_total_time())
            print("Ejecutando...")
            self.name_algorithm.set("RAM - " + self.configure_algorithm_combo.get())
            self.name_mmu.set("MMU - " + self.configure_algorithm_combo.get())
            self.init_tables()
            
            
            self.execute_instruction()
        
    def execute_instruction(self):
            if self.file_processor.instruction_list:
                self.file_processor.process_instruction()
                self.init_statistics()
                
                print("PAGES")
                print(self.file_processor.selected_mmu.get_pages_map())
                print()
                print("PROCESS:")
                print(self.file_processor.selected_mmu.get_process_map())
                print("-------------------------------------")
                print(self.file_processor.selected_mmu.get_table_info())
                print("#####################################")
                
            self.after(1000,self.execute_instruction)

    def init_statistics(self):
            #OPT
            self.processes_opt.set(self.dic_MMU_OPT["processes"])
            self.sim_time_opt .set(self.dic_MMU_OPT["sim-time"])
            self.ram_kb_opt .set(self.dic_MMU_OPT["ram-kb"])
            self.ram_percentage_opt .set(self.dic_MMU_OPT["ram-percentage"])
            self.v_ram_kb_opt .set(self.dic_MMU_OPT["v-ram-kb"])
            self.v_ram_percentage_opt .set(self.dic_MMU_OPT["v-ram-percentage"])
            self.loaded_pages_opt .set(self.dic_MMU_OPT["pages"]["loaded"])
            self.unloaded_pages_opt .set(self.dic_MMU_OPT["pages"]["unloaded"])
            self.seconds_thrashing_opt .set(self.dic_MMU_OPT["thrashing"]["seconds"])
            self.percentage_thrashing_opt .set(self.dic_MMU_OPT["thrashing"]["percentage"])
            self.fragmentacion_opt .set(self.dic_MMU_OPT["fragmentacion"])
            
            #ALG
            self.processes_alg.set(str(self.file_processor.selected_mmu.get_num_process()))
            self.sim_time_alg.set(str(self.file_processor.selected_mmu.get_total_time()) + "s")
            self.ram_kb_alg.set(str(self.file_processor.selected_mmu.get_ram_in_kb()))
            self.ram_percentage_alg.set(str(self.file_processor.selected_mmu.get_ram_in_percentage()))
            self.v_ram_kb_alg.set(str(self.file_processor.selected_mmu.get_vram_in_kb()))
            self.v_ram_percentage_alg.set(str(self.file_processor.selected_mmu.get_vram_in_percentage()))
            self.loaded_pages_alg.set(self.dic_MMU_ALG["pages"]["loaded"])
            self.unloaded_pages_alg.set(self.dic_MMU_ALG["pages"]["unloaded"])
            self.seconds_thrashing_alg.set(str(self.file_processor.selected_mmu.get_trashing_time()))
            self.percentage_thrashing_alg.set(str(self.file_processor.selected_mmu.get_trashing_time_percentage()))
            self.fragmentacion_alg.set(str(self.file_processor.selected_mmu.get_fragmentation()))
            
    def initial_configurations(self):
            # Window Title
            self.title("Proyecto 2 - Sistemas Operativos")

            # Frames create
            self.section_configure = customtkinter.CTkFrame(self, width=1300, height=100)
            self.section_configure.pack()
            
            self.section_ram = customtkinter.CTkFrame(self, width=1300, height=100)
            self.section_ram.pack()
            
            self.section_data = customtkinter.CTkFrame(self, width=1300, height=600)
            self.section_data.pack()
            
            self.section_data_opt = customtkinter.CTkFrame(self.section_data, width=650, height=600)
            self.section_data_opt.pack(side=tk.LEFT)
            
            self.section_data_alg = customtkinter.CTkFrame(self.section_data, width=650, height=600)
            self.section_data_alg.pack(side=tk.RIGHT)
            
            self.section_data_opt_table = customtkinter.CTkScrollableFrame(self.section_data_opt, width=628, height=400)
            self.section_data_opt_table.pack(side=tk.TOP)
            
            self.section_data_opt_statistics = customtkinter.CTkFrame(self.section_data_opt, width=650, height=200)
            self.section_data_opt_statistics.pack(side=tk.BOTTOM)
            
            self.section_data_alg_table = customtkinter.CTkScrollableFrame(self.section_data_alg, width=628, height=400)
            self.section_data_alg_table.pack(side=tk.TOP)
            
            self.section_data_alg_statistics = customtkinter.CTkFrame(self.section_data_alg, width=650, height=200)
            self.section_data_alg_statistics.pack(side=tk.BOTTOM)
            

            #Configure Widgets
            #Label
            self.configure_title = customtkinter.CTkLabel(self.section_configure, text="Ingrese los siguientes parámetros al sistema:", font=("Constantia",15))
            self.configure_subtitle_seed = customtkinter.CTkLabel(self.section_configure, text="Semilla:", font=("Constantia",15))
            self.configure_subtitle_algorithm = customtkinter.CTkLabel(self.section_configure, text="Algorimo:", font=("Constantia",15))
            self.configure_subtitle_file = customtkinter.CTkLabel(self.section_configure, text="Archivo: (Opcional)", font=("Constantia",15))
            self.configure_subtitle_process_number = customtkinter.CTkLabel(self.section_configure, text="Cantidad de procesos:", font=("Constantia",15))
            self.configure_subtitle_operation_number = customtkinter.CTkLabel(self.section_configure, text="Cantidad de operaciones:", font=("Constantia",15))
            
            #Entry
            self.configure_seed_entry = customtkinter.CTkEntry(self.section_configure, width=100)
            self.configure_file_entry = customtkinter.CTkEntry(self.section_configure ,textvariable=self.name_file, state="disabled" , width=350)
            
            #ComboBox
            self.options_algorithm = ["FIFO", "SC", "MRU", "RND"]
            self.options_process = ["10", "50", "100"]
            self.options_operation = ["500", "1000", "5000"]
            
            self.configure_algorithm_combo = customtkinter.CTkComboBox(self.section_configure, values=self.options_algorithm, width = 80)
            self.configure_process_combo = customtkinter.CTkComboBox(self.section_configure, values=self.options_process, width = 170)
            self.configure_operations_combo = customtkinter.CTkComboBox(self.section_configure, values=self.options_operation, width = 195)
            
            #Buttons
            self.configure_file_button = customtkinter.CTkButton(self.section_configure, text="Subir Archivo", command= self.upload_file, width = 100)
            self.configure_execute_button = customtkinter.CTkButton(self.section_configure, text="Ejecutar programa", command=self.execute_program)
            
            #Place Labels
            self.configure_title.place(x = 5, y = 0)
            self.configure_subtitle_algorithm.place(x = 5, y = 25)
            self.configure_subtitle_process_number.place(x = 100, y = 25)
            self.configure_subtitle_operation_number.place(x = 285, y = 25)
            self.configure_subtitle_seed.place(x = 490, y = 25)
            self.configure_subtitle_file.place(x = 610, y = 25)
            
            #Place Entries
            self.configure_seed_entry.place(x = 490, y = 50)
            self.configure_file_entry.place(x = 610, y = 50)
            
            #Place Combobox
            self.configure_algorithm_combo.place(x = 5, y = 50)
            self.configure_process_combo.place(x = 100, y = 50)
            self.configure_operations_combo.place(x = 285, y = 50)
            
            #Place Buttons
            self.configure_file_button.place(x = 970, y = 50)
            self.configure_execute_button.place(x = 1100, y = 50)
            
            #Section Ram Widgets
            #Labels
            self.section_ram_opt_label = customtkinter.CTkLabel(self.section_ram, text="RAM - OPT", font=("Constantia",15))
            self.section_ram_alg_label = customtkinter.CTkLabel(self.section_ram, textvariable=self.name_algorithm, font=("Constantia",15))

            #Table Configure
            self.section_ram.grid_rowconfigure(0,weight=1)
            self.section_ram.grid_columnconfigure((0,1), weight=1)
            
            self.section_ram_opt_label.grid(row=0,column=0,columnspan=100, sticky="nsew")
            for i in range(100):
                frame = customtkinter.CTkFrame(self.section_ram,width=13, height=13, corner_radius=0, fg_color="gray")
                frame.grid(row=1, column= i)
                
            self.section_ram_alg_label.grid(row = 3, column = 0, columnspan = 100, sticky="nsew")
            for i in range(100):
                frame = customtkinter.CTkFrame(self.section_ram,width=13, height=13, corner_radius=0, fg_color="gray")
                frame.grid(row=4, column= i)
                
            #Section Data OPT
            #Frames
            self.frame_label_opt = customtkinter.CTkFrame(self.section_data_opt_table, fg_color="#363b41", width=100, height=20)
            self.frame_label_alg = customtkinter.CTkFrame(self.section_data_alg_table, fg_color="#363b41", width=100, height=20)
            
            #Labels
            self.section_data_opt_label = customtkinter.CTkLabel(self.frame_label_opt, text="MMU - OPT", font=("Constantia",15),text_color="white", width=650, height=20)
            self.section_data_alg_label = customtkinter.CTkLabel(self.frame_label_alg, textvariable=self.name_mmu, font=("Constantia",15),text_color="white", width=650, height=20)
            
            #Place
            self.section_data_opt_label.place(x = 0, y = 0)
            self.section_data_alg_label.place(x = 0, y = 0)
            
            #Table Configure
            self.section_data_opt_table.grid_rowconfigure(0, weight=1)
            self.section_data_opt_table.grid_columnconfigure((0,1), weight=1)
            
            self.section_data_alg_table.grid_rowconfigure(0, weight=1)
            self.section_data_alg_table.grid_columnconfigure((0,1), weight=1)
            
            self.frame_label_opt.grid(row = 0, column=0, columnspan=8, sticky="nsew")
            self.frame_label_alg.grid(row = 0, column=0, columnspan=8, sticky="nsew")
            
            #Load table headers
            for i in range(1):
                for j in range(8):
                    if j % 2 == 0:
                        frame = customtkinter.CTkFrame(self.section_data_opt_table, width=80, height=20, corner_radius=0, fg_color="#363b41")
                        label = customtkinter.CTkLabel(frame, text= self.list_MMU_OPT[i][j], font=("Constantia",14), text_color="white")
                    else:
                        frame = customtkinter.CTkFrame(self.section_data_opt_table, width=80, height=20, corner_radius=0, fg_color="#3e464d")
                        label = customtkinter.CTkLabel(frame, text= self.list_MMU_OPT[i][j], font=("Constantia",14), text_color="white")
                    label.place(x=0, y=0)
                    frame.grid(row = i+1, column=j, sticky="nsew")
                    
            for i in range(1):
                for j in range(8):
                    if j % 2 == 0:
                        frame = customtkinter.CTkFrame(self.section_data_alg_table, width=80, height=20, corner_radius=0, fg_color="#363b41")
                        label = customtkinter.CTkLabel(frame, text= self.list_MMU_ALG[i][j], font=("Constantia",14), text_color="white")
                    else:
                        frame = customtkinter.CTkFrame(self.section_data_alg_table, width=80, height=20, corner_radius=0, fg_color="#3e464d")
                        label = customtkinter.CTkLabel(frame, text= self.list_MMU_ALG[i][j], font=("Constantia",14), text_color="white")
                    label.place(x=0, y=0)
                    frame.grid(row = i+1, column=j, sticky="nsew")
        
        # Load data table
    
    def init_tables(self):
            for i in range(1,len(self.list_MMU_OPT)):
                for j in range(8):
                    frame = customtkinter.CTkFrame(self.section_data_opt_table, width=80, height=20, corner_radius=0, fg_color=self.list_MMU_OPT[i][8][0])
                    label = customtkinter.CTkLabel(frame, text= self.list_MMU_OPT[i][j], font=("Constantia",14), text_color=self.list_MMU_OPT[i][8][1])
                    
                    label.place(x=0, y=0)
                    frame.grid(row = i+1, column=j, sticky="nsew")
                    
            for i in range(1,len(self.list_MMU_ALG)):
                for j in range(8):
                    frame = customtkinter.CTkFrame(self.section_data_alg_table, width=80, height=20, corner_radius=0, fg_color=self.list_MMU_ALG[i][8][0])
                    label = customtkinter.CTkLabel(frame, text= self.list_MMU_ALG[i][j], font=("Constantia",14), text_color=self.list_MMU_ALG[i][8][1])
                    
                    label.place(x=0, y=0)
                    frame.grid(row = i+1, column=j, sticky="nsew")
                
        #Statistics
        
        #Frames
        
    def another_init(self):        
        self.frame_processes_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=325, height=25, border_width=0)
        self.frame_sim_time_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=325, height=25, border_width=0)
        self.frame_ram_kb_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width=0)
        self.frame_ram_percentage_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width=0)
        self.frame_v_ram_kb_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width=0)
        self.frame_v_ram_percentage_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width=0)
        self.frame_pages_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=325, height=25, border_width=0)
        self.frame_pages_child_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=325, height=50, border_width=0)
        self.frame_loaded_opt_label = customtkinter.CTkFrame(self.frame_pages_child_opt_label, width=162.5, height=25, border_width=0)
        self.frame_unloaded_opt_label = customtkinter.CTkFrame(self.frame_pages_child_opt_label, width=162.5, height=25, border_width=0)
        self.frame_thrashing_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width=0)
        self.frame_fragmentacion_opt_label = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width=0)
        
        self.frame_processes_opt_data = customtkinter.CTkFrame(self.section_data_opt_statistics, width=325, height=25, border_width=0, fg_color="#242424")
        self.frame_sim_time_opt_data = customtkinter.CTkFrame(self.section_data_opt_statistics, width=325, height=25, border_width = 0, fg_color="#242424")
        self.frame_ram_kb_opt_data = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_ram_percentage_opt_data = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_v_ram_kb_opt_data = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_v_ram_percentage_opt_data = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_loaded_opt_data = customtkinter.CTkFrame(self.frame_pages_child_opt_label, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_unloaded_opt_data = customtkinter.CTkFrame(self.frame_pages_child_opt_label, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_thrashing_opt_data = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=50, border_width = 0, fg_color="#242424")
        self.frame_thrashing_opt_data_seconds = customtkinter.CTkFrame(self.frame_thrashing_opt_data, width=81.25, height=50, border_width = 0, fg_color="#242424")
        self.frame_thrashing_opt_data_percentage = customtkinter.CTkFrame(self.frame_thrashing_opt_data, width=81.25, height=50, border_width = 0, fg_color="#242424")
        self.frame_fragmentacion_opt_data = customtkinter.CTkFrame(self.section_data_opt_statistics, width=162.5, height=50, border_width = 0, fg_color="#242424")
        
        self.frame_processes_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=325, height=25, border_width=0)
        self.frame_sim_time_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=325, height=25, border_width=0)
        self.frame_ram_kb_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width=0)
        self.frame_ram_percentage_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width=0)
        self.frame_v_ram_kb_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width=0)
        self.frame_v_ram_percentage_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width=0)
        self.frame_pages_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=325, height=25, border_width=0)
        self.frame_pages_child_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=325, height=50, border_width=0)
        self.frame_loaded_alg_label = customtkinter.CTkFrame(self.frame_pages_child_alg_label, width=162.5, height=25, border_width=0)
        self.frame_unloaded_alg_label = customtkinter.CTkFrame(self.frame_pages_child_alg_label, width=162.5, height=25, border_width=0)
        self.frame_thrashing_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width=0)
        self.frame_fragmentacion_alg_label = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width=0)
        
        self.frame_processes_alg_data = customtkinter.CTkFrame(self.section_data_alg_statistics, width=325, height=25, border_width = 0, fg_color="#242424")
        self.frame_sim_time_alg_data = customtkinter.CTkFrame(self.section_data_alg_statistics, width=325, height=25, border_width = 0, fg_color="#242424")
        self.frame_ram_kb_alg_data = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_ram_percentage_alg_data = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_v_ram_kb_alg_data = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_v_ram_percentage_alg_data = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_loaded_alg_data = customtkinter.CTkFrame(self.frame_pages_child_alg_label, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_unloaded_alg_data = customtkinter.CTkFrame(self.frame_pages_child_alg_label, width=162.5, height=25, border_width = 0, fg_color="#242424")
        self.frame_thrashing_alg_data = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=50, border_width = 0, fg_color="#242424")
        self.frame_thrashing_alg_data_seconds = customtkinter.CTkFrame(self.frame_thrashing_alg_data, width=81.25, height=50, border_width = 0, fg_color="#242424")
        self.frame_thrashing_alg_data_percentage = customtkinter.CTkFrame(self.frame_thrashing_alg_data, width=81.25, height=50, border_width = 0, fg_color="#242424")
        self.frame_fragmentacion_alg_data = customtkinter.CTkFrame(self.section_data_alg_statistics, width=162.5, height=50, border_width = 0, fg_color="#242424")
        
        self.frame_loaded_opt_label.grid(row=0, column=0, sticky="nsew")
        self.frame_unloaded_opt_label.grid(row=0, column=1, sticky="nsew")
        self.frame_loaded_opt_data.grid(row=1, column=0, sticky="nsew")
        self.frame_unloaded_opt_data.grid(row=1, column=1, sticky="nsew")

        self.frame_thrashing_opt_data_seconds.grid(row=0, column=0, sticky="nsew")
        self.frame_thrashing_opt_data_percentage.grid(row=0, column=1, sticky="nsew")
       
        self.frame_loaded_alg_label.grid(row=0, column=0, sticky="nsew")
        self.frame_unloaded_alg_label.grid(row=0, column=1, sticky="nsew")
        self.frame_loaded_alg_data.grid(row=1, column=0, sticky="nsew")
        self.frame_unloaded_alg_data.grid(row=1, column=1, sticky="nsew")
        
        self.frame_thrashing_alg_data_seconds.grid(row=0, column=0, sticky="nsew")
        self.frame_thrashing_alg_data_percentage.grid(row=0, column=1, sticky="nsew")
        
        
        #Labels
        self.statistics_processes_opt_label = customtkinter.CTkLabel(self.frame_processes_opt_label, text="Processes", font=("Constantia",15), width=325)
        self.statistics_sim_time_opt_label = customtkinter.CTkLabel(self.frame_sim_time_opt_label, text="Sim-Time", font=("Constantia",15), width=325)
        self.statistics_ram_kb_opt_label = customtkinter.CTkLabel(self.frame_ram_kb_opt_label, text="RAM KB", font=("Constantia",15), width=162.5)
        self.statistics_ram_percentage_opt_label = customtkinter.CTkLabel(self.frame_ram_percentage_opt_label, text="RAM %", font=("Constantia",15), width=162.5)
        self.statistics_v_ram_kb_opt_label = customtkinter.CTkLabel(self.frame_v_ram_kb_opt_label, text="V-RAM KB", font=("Constantia",15), width=162.5)
        self.statistics_v_ram_percentage_opt_label = customtkinter.CTkLabel(self.frame_v_ram_percentage_opt_label, text="V-RAM-%", font=("Constantia",15), width=162.5)
        self.statistics_pages_opt_label = customtkinter.CTkLabel(self.frame_pages_opt_label, text="PAGES", font=("Constantia",15), width=325)
        self.statistics_loaded_opt_label = customtkinter.CTkLabel(self.frame_loaded_opt_label, text="LOADED", font=("Constantia",15), width=165.5)
        self.statistics_unloaded_opt_label = customtkinter.CTkLabel(self.frame_unloaded_opt_label, text="UNLOADED", font=("Constantia",15), width=165.5)
        self.statistics_thrashing_opt_label = customtkinter.CTkLabel(self.frame_thrashing_opt_label, text="Thrashing", font=("Constantia",15), width=165.5)
        self.statistics_fragmentacion_opt_label = customtkinter.CTkLabel(self.frame_fragmentacion_opt_label, text="Fragmentacion", font=("Constantia",15), width=165.5)
        
        self.statistics_processes_opt_data = customtkinter.CTkLabel(self.frame_processes_opt_data, textvariable = self.processes_opt, font=("Constantia",15), width=325)
        self.statistics_sim_time_opt_data = customtkinter.CTkLabel(self.frame_sim_time_opt_data, textvariable = self.sim_time_opt, font=("Constantia",15), width=325)
        self.statistics_ram_kb_opt_data = customtkinter.CTkLabel(self.frame_ram_kb_opt_data, textvariable=self.ram_kb_opt, font=("Constantia",15), width=162.5)
        self.statistics_ram_percentage_opt_data = customtkinter.CTkLabel(self.frame_ram_percentage_opt_data, textvariable= self.ram_percentage_opt, font=("Constantia",15), width=162.5)
        self.statistics_v_ram_kb_opt_data = customtkinter.CTkLabel(self.frame_v_ram_kb_opt_data, textvariable = self.v_ram_kb_opt, font=("Constantia",15), width=162.5)
        self.statistics_v_ram_percentage_opt_data = customtkinter.CTkLabel(self.frame_v_ram_percentage_opt_data, textvariable = self.v_ram_percentage_opt, font=("Constantia",15), width=162.5)
        self.statistics_loaded_opt_data = customtkinter.CTkLabel(self.frame_loaded_opt_data, textvariable= self.loaded_pages_opt, font=("Constantia",15), width=162.5)
        self.statistics_unloaded_opt_data = customtkinter.CTkLabel(self.frame_unloaded_opt_data, textvariable = self.unloaded_pages_opt, font=("Constantia",15), width=162.5)
        self.statistics_thrashing_opt_data_seconds = customtkinter.CTkLabel(self.frame_thrashing_opt_data_seconds, textvariable= self.seconds_thrashing_opt, font=("Constantia",15), width=81.25, height=50)
        self.statistics_thrashing_opt_data_percentage = customtkinter.CTkLabel(self.frame_thrashing_opt_data_percentage, textvariable= self.percentage_thrashing_opt, font=("Constantia",15), width=81.25, height=50)
        self.statistics_fragmentacion_opt_data = customtkinter.CTkLabel(self.frame_fragmentacion_opt_data, textvariable = self.fragmentacion_opt, font=("Constantia",15), width= 162.5, height=50)
        
        #
        
        self.statistics_processes_alg_label = customtkinter.CTkLabel(self.frame_processes_alg_label, text="Processess", font=("Constantia",15), width=325)
        self.statistics_sim_time_alg_label = customtkinter.CTkLabel(self.frame_sim_time_alg_label, text="Sim-Time", font=("Constantia",15), width=325)
        self.statistics_ram_kb_alg_label = customtkinter.CTkLabel(self.frame_ram_kb_alg_label, text="RAM KB", font=("Constantia",15), width=162.5)
        self.statistics_ram_percentage_alg_label = customtkinter.CTkLabel(self.frame_ram_percentage_alg_label, text="RAM %", font=("Constantia",15), width=162.5)
        self.statistics_v_ram_kb_alg_label = customtkinter.CTkLabel(self.frame_v_ram_kb_alg_label, text="V-RAM KB", font=("Constantia",15), width=162.5)
        self.statistics_v_ram_percentage_alg_label = customtkinter.CTkLabel(self.frame_v_ram_percentage_alg_label, text="V-RAM-%", font=("Constantia",15), width=162.5)
        self.statistics_pages_alg_label = customtkinter.CTkLabel(self.frame_pages_alg_label, text="PAGES", font=("Constantia",15), width=325)
        self.statistics_loaded_alg_label = customtkinter.CTkLabel(self.frame_loaded_alg_label, text="LOADED", font=("Constantia",15), width=165.5)
        self.statistics_unloaded_alg_label = customtkinter.CTkLabel(self.frame_unloaded_alg_label, text="UNLOADED", font=("Constantia",15), width=165.5)
        self.statistics_thrashing_alg_label = customtkinter.CTkLabel(self.frame_thrashing_alg_label, text="Thrashing", font=("Constantia",15), width=165.5)
        self.statistics_fragmentacion_alg_label = customtkinter.CTkLabel(self.frame_fragmentacion_alg_label, text="Fragmentacion", font=("Constantia",15), width=165.5)
        
        self.statistics_processes_alg_data = customtkinter.CTkLabel(self.frame_processes_alg_data, textvariable= self.processes_alg, font=("Constantia",15), width=325)
        self.statistics_sim_time_alg_data = customtkinter.CTkLabel(self.frame_sim_time_alg_data, textvariable = self.sim_time_alg, font=("Constantia",15), width=325)
        self.statistics_ram_kb_alg_data = customtkinter.CTkLabel(self.frame_ram_kb_alg_data, textvariable = self.ram_kb_alg, font=("Constantia",15), width=162.5)
        self.statistics_ram_percentage_alg_data = customtkinter.CTkLabel(self.frame_ram_percentage_alg_data, textvariable = self.ram_percentage_alg, font=("Constantia",15), width=162.5)
        self.statistics_v_ram_kb_alg_data = customtkinter.CTkLabel(self.frame_v_ram_kb_alg_data, textvariable= self.v_ram_kb_alg, font=("Constantia",15), width=162.5)
        self.statistics_v_ram_percentage_alg_data = customtkinter.CTkLabel(self.frame_v_ram_percentage_alg_data, textvariable= self.v_ram_percentage_alg, font=("Constantia",15), width=162.5)
        self.statistics_loaded_alg_data = customtkinter.CTkLabel(self.frame_loaded_alg_data, textvariable= self.loaded_pages_alg, font=("Constantia",15), width=162.5)
        self.statistics_unloaded_alg_data = customtkinter.CTkLabel(self.frame_unloaded_alg_data, textvariable= self.unloaded_pages_alg, font=("Constantia",15), width=162.5)
        self.statistics_thrashing_alg_data_seconds = customtkinter.CTkLabel(self.frame_thrashing_alg_data_seconds, textvariable= self.seconds_thrashing_alg , font=("Constantia",15), width=81.25, height=50)
        self.statistics_thrashing_alg_data_percentage = customtkinter.CTkLabel(self.frame_thrashing_alg_data_percentage, textvariable = self.percentage_thrashing_alg, font=("Constantia",15), width=81.25, height=50)
        self.statistics_fragmentacion_alg_data = customtkinter.CTkLabel(self.frame_fragmentacion_alg_data, textvariable = self.fragmentacion_alg, font=("Constantia",15), width= 162.5, height=50)
        
        #Place
        self.statistics_processes_opt_label.place(x = 0, y = 0)
        self.statistics_sim_time_opt_label.place(x = 0, y = 0)
        self.statistics_ram_kb_opt_label.place(x = 0, y = 0)
        self.statistics_ram_percentage_opt_label.place(x = 0, y = 0)
        self.statistics_v_ram_kb_opt_label.place(x = 0, y = 0)
        self.statistics_v_ram_percentage_opt_label.place(x = 0, y = 0)
        
        self.statistics_pages_opt_label.place(x = 0, y = 0)
        self.statistics_loaded_opt_label.place(x = 0, y = 0)
        self.statistics_unloaded_opt_label.place(x = 0, y = 0)
        self.statistics_thrashing_opt_label.place(x = 0, y = 0)
        self.statistics_fragmentacion_opt_label.place(x = 0, y = 0)
        
        self.statistics_processes_opt_data.place(x = 0, y = 0)
        self.statistics_sim_time_opt_data.place(x = 0, y = 0)
        self.statistics_ram_kb_opt_data.place(x = 0, y = 0)
        self.statistics_ram_percentage_opt_data.place(x = 0, y = 0)
        self.statistics_v_ram_kb_opt_data.place(x = 0, y = 0)
        self.statistics_v_ram_percentage_opt_data.place(x = 0, y = 0)
        
        self.statistics_loaded_opt_data.place(x = 0, y = 0)
        self.statistics_unloaded_opt_data.place(x = 0, y = 0)
        self.statistics_thrashing_opt_data_seconds.place(x = 0, y = 0)
        self.statistics_thrashing_opt_data_percentage.place(x = 0, y = 0)
        self.statistics_fragmentacion_opt_data.place(x = 0, y = 0)
        
        #
        
        self.statistics_processes_alg_label.place(x = 0, y = 0)
        self.statistics_sim_time_alg_label.place(x = 0, y = 0)
        self.statistics_ram_kb_alg_label.place(x = 0, y = 0)
        self.statistics_ram_percentage_alg_label.place(x = 0, y = 0)
        self.statistics_v_ram_kb_alg_label.place(x = 0, y = 0)
        self.statistics_v_ram_percentage_alg_label.place(x = 0, y = 0)
        
        self.statistics_pages_alg_label.place(x = 0, y = 0)
        self.statistics_loaded_alg_label.place(x = 0, y = 0)
        self.statistics_unloaded_alg_label.place(x = 0, y = 0)
        self.statistics_thrashing_alg_label.place(x = 0, y = 0)
        self.statistics_fragmentacion_alg_label.place(x = 0, y = 0)
        
        self.statistics_processes_alg_data.place(x = 0, y = 0)
        self.statistics_sim_time_alg_data.place(x = 0, y = 0)
        self.statistics_ram_kb_alg_data.place(x = 0, y = 0)
        self.statistics_ram_percentage_alg_data.place(x = 0, y = 0)
        self.statistics_v_ram_kb_alg_data.place(x = 0, y = 0)
        self.statistics_v_ram_percentage_alg_data.place(x = 0, y = 0)
        
        self.statistics_loaded_alg_data.place(x = 0, y = 0)
        self.statistics_unloaded_alg_data.place(x = 0, y = 0)
        self.statistics_thrashing_alg_data_seconds.place(x = 0, y = 0)
        self.statistics_thrashing_alg_data_percentage.place(x = 0, y = 0)
        self.statistics_fragmentacion_alg_data.place(x = 0, y = 0)
        
        
        
        
        #Table configure
        
        self.section_data_opt_statistics.grid_rowconfigure(0, weight=1)
        self.section_data_opt_statistics.grid_columnconfigure((0,1), weight=1)

        self.frame_processes_opt_label.grid(row = 0, column = 0, columnspan = 2, sticky="nsew")
        self.frame_sim_time_opt_label.grid(row = 0, column = 2, columnspan = 2, sticky="nsew")
        self.frame_ram_kb_opt_label.grid(row = 2, column = 0, sticky="nsew")
        self.frame_ram_percentage_opt_label.grid(row = 2, column = 1, sticky="nsew")
        self.frame_v_ram_kb_opt_label.grid(row = 2, column = 2, sticky="nsew")
        self.frame_v_ram_percentage_opt_label.grid(row = 2, column = 3, sticky="nsew")
        self.frame_pages_opt_label.grid(row = 4, column = 0,columnspan=2, sticky="nsew")
        self.frame_thrashing_opt_label.grid(row = 4, column = 2, sticky="nsew")
        self.frame_fragmentacion_opt_label.grid(row = 4, column = 3, sticky="nsew")
        
        self.frame_processes_opt_data.grid(row = 1, column = 0, columnspan = 2, sticky="nsew")
        self.frame_sim_time_opt_data.grid(row = 1, column = 2, columnspan = 2, sticky="nsew")
        self.frame_ram_kb_opt_data.grid(row = 3, column = 0, sticky="nsew")
        self.frame_ram_percentage_opt_data.grid(row = 3, column = 1, sticky="nsew")
        self.frame_v_ram_kb_opt_data.grid(row = 3, column = 2, sticky="nsew")
        self.frame_v_ram_percentage_opt_data.grid(row = 3, column = 3, sticky="nsew")
        self.frame_pages_child_opt_label.grid(row = 5, column = 0,rowspan=2 , columnspan = 2, sticky="nsew")
        self.frame_thrashing_opt_data.grid(row=5, column=2, rowspan=2, sticky="nsew")
        self.frame_fragmentacion_opt_data.grid(row=5, column=3, rowspan=2, sticky="nsew")
        
        #
        
        self.section_data_alg_statistics.grid_rowconfigure(0, weight=1)
        self.section_data_alg_statistics.grid_columnconfigure((0,1), weight=1)
        
        self.frame_processes_alg_label.grid(row = 0, column = 0, columnspan = 2, sticky="nsew")
        self.frame_sim_time_alg_label.grid(row = 0, column = 2, columnspan = 2, sticky="nsew")
        self.frame_ram_kb_alg_label.grid(row = 2, column = 0, sticky="nsew")
        self.frame_ram_percentage_alg_label.grid(row = 2, column = 1, sticky="nsew")
        self.frame_v_ram_kb_alg_label.grid(row = 2, column = 2, sticky="nsew")
        self.frame_v_ram_percentage_alg_label.grid(row = 2, column = 3, sticky="nsew")
        self.frame_pages_alg_label.grid(row = 4, column = 0,columnspan=2, sticky="nsew")
        self.frame_thrashing_alg_label.grid(row = 4, column = 2, sticky="nsew")
        self.frame_fragmentacion_alg_label.grid(row = 4, column = 3, sticky="nsew")
        
        self.frame_processes_alg_data.grid(row = 1, column = 0, columnspan = 2, sticky="nsew")
        self.frame_sim_time_alg_data.grid(row = 1, column = 2, columnspan = 2, sticky="nsew")
        self.frame_ram_kb_alg_data.grid(row = 3, column = 0, sticky="nsew")
        self.frame_ram_percentage_alg_data.grid(row = 3, column = 1, sticky="nsew")
        self.frame_v_ram_kb_alg_data.grid(row = 3, column = 2, sticky="nsew")
        self.frame_v_ram_percentage_alg_data.grid(row = 3, column = 3, sticky="nsew")
        self.frame_pages_child_alg_label.grid(row = 5, column = 0,rowspan=2 , columnspan = 2, sticky="nsew")
        self.frame_thrashing_alg_data.grid(row=5, column=2, rowspan=2, sticky="nsew")
        self.frame_fragmentacion_alg_data.grid(row=5, column=3, rowspan=2, sticky="nsew")
                
              

# Ejecutar el bucle principal
test_class = main_proyect()
