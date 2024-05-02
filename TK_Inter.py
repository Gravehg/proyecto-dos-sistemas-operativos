import tkinter as tk
import customtkinter
from FileProcessor import FileProcessor
from FileGenerator import FileGenerator
from tkinter.filedialog import askopenfile


#Window TkInter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
window = customtkinter.CTk()

# Variables
list_MMU_OPT = [('PAGE ID', 'PID', 'LOADED', 'L-ADDR', 'M-ADDR', 'D-ADDR', 'LOADED-T', 'MARK'),
                ('1','1','X','1','1','-','0s','-', ("yellow", "black")),] 
list_MMU_ALG = [('PAGE ID', 'PID', 'LOADED', 'L-ADDR', 'M-ADDR', 'D-ADDR', 'LOADED-T', 'MARK'),
                ('1','1','X','1','1','-','0s','-', ("yellow", "black")),]
dic_MMU_OPT = {
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
dic_MMU_ALG = {
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

name_file = tk.StringVar()
name_algorithm = tk.StringVar()
name_mmu = tk.StringVar()
name_algorithm.set("RAM - [ALG]")
name_mmu.set("MMU - [ALG]")

#Statistics Change Variables
processes_opt = tk.StringVar()
sim_time_opt = tk.StringVar()
ram_kb_opt = tk.StringVar()
ram_percentage_opt = tk.StringVar()
v_ram_kb_opt = tk.StringVar()
v_ram_percentage_opt = tk.StringVar()
loaded_pages_opt = tk.StringVar()
unloaded_pages_opt = tk.StringVar()
seconds_thrashing_opt = tk.StringVar()
percentage_thrashing_opt = tk.StringVar()
fragmentacion_opt = tk.StringVar()

processes_alg = tk.StringVar()
sim_time_alg = tk.StringVar()
ram_kb_alg = tk.StringVar()
ram_percentage_alg = tk.StringVar()
v_ram_kb_alg = tk.StringVar()
v_ram_percentage_alg = tk.StringVar()
loaded_pages_alg = tk.StringVar()
unloaded_pages_alg = tk.StringVar()
seconds_thrashing_alg = tk.StringVar()
percentage_thrashing_alg = tk.StringVar()
fragmentacion_alg = tk.StringVar()

processes_opt.set("-")
sim_time_opt.set("-")
ram_kb_opt.set("-")
ram_percentage_opt.set("-")
v_ram_kb_opt.set("-")
v_ram_percentage_opt.set("-")
loaded_pages_opt.set("-")
unloaded_pages_opt.set("-")
seconds_thrashing_opt.set("-")
percentage_thrashing_opt.set("-")
fragmentacion_opt.set("-")

processes_alg.set("-")
sim_time_alg.set("-")
ram_kb_alg.set("-")
ram_percentage_alg.set("-")
v_ram_kb_alg.set("-")
v_ram_percentage_alg.set("-")
loaded_pages_alg.set("-")
unloaded_pages_alg.set("-")
seconds_thrashing_alg.set("-")
percentage_thrashing_alg.set("-")
fragmentacion_alg.set("-")


class main_proyect():
    
    def __init__(self, window):
        self.file_processor = None
        self.file_generator = None
        self.selected_file = None
        global name_file
        global name_algorithm
        global name_mmu
        
        global processes_opt
        global sim_time_opt
        global ram_kb_opt
        global ram_percentage_opt
        global v_ram_kb_opt
        global v_ram_percentage_opt
        global loaded_pages_opt
        global unloaded_pages_opt
        global seconds_thrashing_opt
        global percentage_thrashing_opt
        global fragmentacion_opt
        
        global processes_alg
        global sim_time_alg
        global ram_kb_alg
        global ram_percentage_alg
        global v_ram_kb_alg
        global v_ram_percentage_alg
        global loaded_pages_alg
        global unloaded_pages_alg
        global seconds_thrashing_alg
        global percentage_thrashing_alg
        global fragmentacion_alg
        
        def upload_file():
            self.selected_file = askopenfile(mode="r", filetypes=[('Archivos de texto', '*.txt')])
            
        def execute_program():
            if self.selected_file is not None:
                self.file_processor = FileProcessor(self.selected_file.name, configure_algorithm_combo.get())
                name_file.set(self.selected_file.name)
            else:
                seed = None
                if not configure_seed_entry.get():
                    seed = 1000
                else:
                    seed = int(configure_seed_entry.get())
                self.file_generator = FileGenerator(int(configure_process_combo.get()),int(configure_operations_combo.get()),seed)
                self.file_generator.generate_file()
                self.file_processor = FileProcessor(self.file_generator.file_name, configure_algorithm_combo.get())
                #Feeds page references to optimal MMU
                self.file_processor.feed_opt_references()
                print(self.file_processor.optimal_mmu.pointer_references)

            #Un tipo wait o algo asi antes de ejecutar la siguiente instruction
            #While len(self.file_processor.instruction) > 0
            # self,file_processor.processes_instruction()
            # wait(algunos_segundos)
            self.file_processor.process_instruction()
            #Sacar las estadisticas la as MMU
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            self.file_processor.process_instruction()
            print(self.file_processor.selected_mmu.get_total_time())
            print("Ejecutando...")
            name_algorithm.set("RAM - " + configure_algorithm_combo.get())
            name_mmu.set("MMU - " + configure_algorithm_combo.get())
            init_tables()
            init_statistics()
            
        def init_statistics():
            processes_opt.set(dic_MMU_OPT["processes"])
            sim_time_opt .set(dic_MMU_OPT["sim-time"])
            ram_kb_opt .set(dic_MMU_OPT["ram-kb"])
            ram_percentage_opt .set(dic_MMU_OPT["ram-percentage"])
            v_ram_kb_opt .set(dic_MMU_OPT["v-ram-kb"])
            v_ram_percentage_opt .set(dic_MMU_OPT["v-ram-percentage"])
            loaded_pages_opt .set(dic_MMU_OPT["pages"]["loaded"])
            unloaded_pages_opt .set(dic_MMU_OPT["pages"]["unloaded"])
            seconds_thrashing_opt .set(dic_MMU_OPT["thrashing"]["seconds"])
            percentage_thrashing_opt .set(dic_MMU_OPT["thrashing"]["percentage"])
            fragmentacion_opt .set(dic_MMU_OPT["fragmentacion"])
            
            processes_alg .set(dic_MMU_ALG["processes"])
            sim_time_alg .set(dic_MMU_ALG["sim-time"])
            ram_kb_alg .set(dic_MMU_ALG["ram-kb"])
            ram_percentage_alg .set(dic_MMU_ALG["ram-percentage"])
            v_ram_kb_alg .set(dic_MMU_ALG["v-ram-kb"])
            v_ram_percentage_alg .set(dic_MMU_ALG["v-ram-percentage"])
            loaded_pages_alg .set(dic_MMU_ALG["pages"]["loaded"])
            unloaded_pages_alg .set(dic_MMU_ALG["pages"]["unloaded"])
            seconds_thrashing_alg .set(dic_MMU_ALG["thrashing"]["seconds"])
            percentage_thrashing_alg .set(dic_MMU_ALG["thrashing"]["percentage"])
            fragmentacion_alg .set(dic_MMU_ALG["fragmentacion"])
            
        
        # Window Title
        window.title("Proyecto 2 - Sistemas Operativos")

        # Frames create
        section_configure = customtkinter.CTkFrame(window, width=1300, height=100)
        section_configure.pack()
        
        section_ram = customtkinter.CTkFrame(window, width=1300, height=100)
        section_ram.pack()
        
        section_data = customtkinter.CTkFrame(window, width=1300, height=600)
        section_data.pack()
        
        section_data_opt = customtkinter.CTkFrame(section_data, width=650, height=600)
        section_data_opt.pack(side=tk.LEFT)
        
        section_data_alg = customtkinter.CTkFrame(section_data, width=650, height=600)
        section_data_alg.pack(side=tk.RIGHT)
        
        section_data_opt_table = customtkinter.CTkScrollableFrame(section_data_opt, width=628, height=400)
        section_data_opt_table.pack(side=tk.TOP)
        
        section_data_opt_statistics = customtkinter.CTkFrame(section_data_opt, width=650, height=200)
        section_data_opt_statistics.pack(side=tk.BOTTOM)
        
        section_data_alg_table = customtkinter.CTkScrollableFrame(section_data_alg, width=628, height=400)
        section_data_alg_table.pack(side=tk.TOP)
        
        section_data_alg_statistics = customtkinter.CTkFrame(section_data_alg, width=650, height=200)
        section_data_alg_statistics.pack(side=tk.BOTTOM)
        

        #Configure Widgets
        #Label
        configure_title = customtkinter.CTkLabel(section_configure, text="Ingrese los siguientes parámetros al sistema:", font=("Constantia",15))
        configure_subtitle_seed = customtkinter.CTkLabel(section_configure, text="Semilla:", font=("Constantia",15))
        configure_subtitle_algorithm = customtkinter.CTkLabel(section_configure, text="Algorimo:", font=("Constantia",15))
        configure_subtitle_file = customtkinter.CTkLabel(section_configure, text="Archivo: (Opcional)", font=("Constantia",15))
        configure_subtitle_process_number = customtkinter.CTkLabel(section_configure, text="Cantidad de procesos:", font=("Constantia",15))
        configure_subtitle_operation_number = customtkinter.CTkLabel(section_configure, text="Cantidad de operaciones:", font=("Constantia",15))
        
        #Entry
        configure_seed_entry = customtkinter.CTkEntry(section_configure, width=100)
        configure_file_entry = customtkinter.CTkEntry(section_configure ,textvariable=name_file, state="disabled" , width=350)
        
        #ComboBox
        options_algorithm = ["FIFO", "SC", "MRU", "RND"]
        options_process = ["10", "50", "100"]
        options_operation = ["500", "1000", "5000"]
        
        configure_algorithm_combo = customtkinter.CTkComboBox(section_configure, values=options_algorithm, width = 80)
        configure_process_combo = customtkinter.CTkComboBox(section_configure, values=options_process, width = 170)
        configure_operations_combo = customtkinter.CTkComboBox(section_configure, values=options_operation, width = 195)
        
        #Buttons
        configure_file_button = customtkinter.CTkButton(section_configure, text="Subir Archivo", command=upload_file, width = 100)
        configure_execute_button = customtkinter.CTkButton(section_configure, text="Ejecutar programa", command=execute_program)
        
        #Place Labels
        configure_title.place(x = 5, y = 0)
        configure_subtitle_algorithm.place(x = 5, y = 25)
        configure_subtitle_process_number.place(x = 100, y = 25)
        configure_subtitle_operation_number.place(x = 285, y = 25)
        configure_subtitle_seed.place(x = 490, y = 25)
        configure_subtitle_file.place(x = 610, y = 25)
        
        #Place Entries
        configure_seed_entry.place(x = 490, y = 50)
        configure_file_entry.place(x = 610, y = 50)
        
        #Place Combobox
        configure_algorithm_combo.place(x = 5, y = 50)
        configure_process_combo.place(x = 100, y = 50)
        configure_operations_combo.place(x = 285, y = 50)
        
        #Place Buttons
        configure_file_button.place(x = 970, y = 50)
        configure_execute_button.place(x = 1100, y = 50)
        
        #Section Ram Widgets
        #Labels
        section_ram_opt_label = customtkinter.CTkLabel(section_ram, text="RAM - OPT", font=("Constantia",15))
        section_ram_alg_label = customtkinter.CTkLabel(section_ram, textvariable=name_algorithm, font=("Constantia",15))

        #Table Configure
        section_ram.grid_rowconfigure(0,weight=1)
        section_ram.grid_columnconfigure((0,1), weight=1)
        
        section_ram_opt_label.grid(row=0,column=0,columnspan=100, sticky="nsew")
        for i in range(100):
            frame = customtkinter.CTkFrame(section_ram,width=13, height=13, corner_radius=0, fg_color="gray")
            frame.grid(row=1, column= i)
            
        section_ram_alg_label.grid(row = 3, column = 0, columnspan = 100, sticky="nsew")
        for i in range(100):
            frame = customtkinter.CTkFrame(section_ram,width=13, height=13, corner_radius=0, fg_color="gray")
            frame.grid(row=4, column= i)
            
        #Section Data OPT
        #Frames
        frame_label_opt = customtkinter.CTkFrame(section_data_opt_table, fg_color="#363b41", width=100, height=20)
        frame_label_alg = customtkinter.CTkFrame(section_data_alg_table, fg_color="#363b41", width=100, height=20)
        
        #Labels
        section_data_opt_label = customtkinter.CTkLabel(frame_label_opt, text="MMU - OPT", font=("Constantia",15),text_color="white", width=650, height=20)
        section_data_alg_label = customtkinter.CTkLabel(frame_label_alg, textvariable=name_mmu, font=("Constantia",15),text_color="white", width=650, height=20)
        
        #Place
        section_data_opt_label.place(x = 0, y = 0)
        section_data_alg_label.place(x = 0, y = 0)
        
        #Table Configure
        section_data_opt_table.grid_rowconfigure(0, weight=1)
        section_data_opt_table.grid_columnconfigure((0,1), weight=1)
        
        section_data_alg_table.grid_rowconfigure(0, weight=1)
        section_data_alg_table.grid_columnconfigure((0,1), weight=1)
        
        frame_label_opt.grid(row = 0, column=0, columnspan=8, sticky="nsew")
        frame_label_alg.grid(row = 0, column=0, columnspan=8, sticky="nsew")
        
        #Load table headers
        for i in range(1):
            for j in range(8):
                if j % 2 == 0:
                    frame = customtkinter.CTkFrame(section_data_opt_table, width=80, height=20, corner_radius=0, fg_color="#363b41")
                    label = customtkinter.CTkLabel(frame, text= list_MMU_OPT[i][j], font=("Constantia",14), text_color="white")
                else:
                    frame = customtkinter.CTkFrame(section_data_opt_table, width=80, height=20, corner_radius=0, fg_color="#3e464d")
                    label = customtkinter.CTkLabel(frame, text= list_MMU_OPT[i][j], font=("Constantia",14), text_color="white")
                label.place(x=0, y=0)
                frame.grid(row = i+1, column=j, sticky="nsew")
                
        for i in range(1):
            for j in range(8):
                if j % 2 == 0:
                    frame = customtkinter.CTkFrame(section_data_alg_table, width=80, height=20, corner_radius=0, fg_color="#363b41")
                    label = customtkinter.CTkLabel(frame, text= list_MMU_ALG[i][j], font=("Constantia",14), text_color="white")
                else:
                    frame = customtkinter.CTkFrame(section_data_alg_table, width=80, height=20, corner_radius=0, fg_color="#3e464d")
                    label = customtkinter.CTkLabel(frame, text= list_MMU_ALG[i][j], font=("Constantia",14), text_color="white")
                label.place(x=0, y=0)
                frame.grid(row = i+1, column=j, sticky="nsew")
        
        # Load data table
        def init_tables():
            for i in range(1,len(list_MMU_OPT)):
                for j in range(8):
                    frame = customtkinter.CTkFrame(section_data_opt_table, width=80, height=20, corner_radius=0, fg_color=list_MMU_OPT[i][8][0])
                    label = customtkinter.CTkLabel(frame, text= list_MMU_OPT[i][j], font=("Constantia",14), text_color=list_MMU_OPT[i][8][1])
                    
                    label.place(x=0, y=0)
                    frame.grid(row = i+1, column=j, sticky="nsew")
                    
            for i in range(1,len(list_MMU_ALG)):
                for j in range(8):
                    frame = customtkinter.CTkFrame(section_data_alg_table, width=80, height=20, corner_radius=0, fg_color=list_MMU_ALG[i][8][0])
                    label = customtkinter.CTkLabel(frame, text= list_MMU_ALG[i][j], font=("Constantia",14), text_color=list_MMU_ALG[i][8][1])
                    
                    label.place(x=0, y=0)
                    frame.grid(row = i+1, column=j, sticky="nsew")
                
        #Statistics
        
        #Frames
        frame_processes_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=325, height=25, border_width=0)
        frame_sim_time_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=325, height=25, border_width=0)
        frame_ram_kb_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width=0)
        frame_ram_percentage_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width=0)
        frame_v_ram_kb_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width=0)
        frame_v_ram_percentage_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width=0)
        frame_pages_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=325, height=25, border_width=0)
        frame_pages_child_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=325, height=50, border_width=0)
        frame_loaded_opt_label = customtkinter.CTkFrame(frame_pages_child_opt_label, width=162.5, height=25, border_width=0)
        frame_unloaded_opt_label = customtkinter.CTkFrame(frame_pages_child_opt_label, width=162.5, height=25, border_width=0)
        frame_thrashing_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width=0)
        frame_fragmentacion_opt_label = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width=0)
        
        frame_processes_opt_data = customtkinter.CTkFrame(section_data_opt_statistics, width=325, height=25, border_width=0, fg_color="#242424")
        frame_sim_time_opt_data = customtkinter.CTkFrame(section_data_opt_statistics, width=325, height=25, border_width = 0, fg_color="#242424")
        frame_ram_kb_opt_data = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_ram_percentage_opt_data = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_v_ram_kb_opt_data = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_v_ram_percentage_opt_data = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_loaded_opt_data = customtkinter.CTkFrame(frame_pages_child_opt_label, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_unloaded_opt_data = customtkinter.CTkFrame(frame_pages_child_opt_label, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_thrashing_opt_data = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=50, border_width = 0, fg_color="#242424")
        frame_thrashing_opt_data_seconds = customtkinter.CTkFrame(frame_thrashing_opt_data, width=81.25, height=50, border_width = 0, fg_color="#242424")
        frame_thrashing_opt_data_percentage = customtkinter.CTkFrame(frame_thrashing_opt_data, width=81.25, height=50, border_width = 0, fg_color="#242424")
        frame_fragmentacion_opt_data = customtkinter.CTkFrame(section_data_opt_statistics, width=162.5, height=50, border_width = 0, fg_color="#242424")
        
        frame_processes_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=325, height=25, border_width=0)
        frame_sim_time_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=325, height=25, border_width=0)
        frame_ram_kb_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width=0)
        frame_ram_percentage_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width=0)
        frame_v_ram_kb_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width=0)
        frame_v_ram_percentage_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width=0)
        frame_pages_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=325, height=25, border_width=0)
        frame_pages_child_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=325, height=50, border_width=0)
        frame_loaded_alg_label = customtkinter.CTkFrame(frame_pages_child_alg_label, width=162.5, height=25, border_width=0)
        frame_unloaded_alg_label = customtkinter.CTkFrame(frame_pages_child_alg_label, width=162.5, height=25, border_width=0)
        frame_thrashing_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width=0)
        frame_fragmentacion_alg_label = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width=0)
        
        frame_processes_alg_data = customtkinter.CTkFrame(section_data_alg_statistics, width=325, height=25, border_width = 0, fg_color="#242424")
        frame_sim_time_alg_data = customtkinter.CTkFrame(section_data_alg_statistics, width=325, height=25, border_width = 0, fg_color="#242424")
        frame_ram_kb_alg_data = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_ram_percentage_alg_data = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_v_ram_kb_alg_data = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_v_ram_percentage_alg_data = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_loaded_alg_data = customtkinter.CTkFrame(frame_pages_child_alg_label, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_unloaded_alg_data = customtkinter.CTkFrame(frame_pages_child_alg_label, width=162.5, height=25, border_width = 0, fg_color="#242424")
        frame_thrashing_alg_data = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=50, border_width = 0, fg_color="#242424")
        frame_thrashing_alg_data_seconds = customtkinter.CTkFrame(frame_thrashing_alg_data, width=81.25, height=50, border_width = 0, fg_color="#242424")
        frame_thrashing_alg_data_percentage = customtkinter.CTkFrame(frame_thrashing_alg_data, width=81.25, height=50, border_width = 0, fg_color="#242424")
        frame_fragmentacion_alg_data = customtkinter.CTkFrame(section_data_alg_statistics, width=162.5, height=50, border_width = 0, fg_color="#242424")
        
        frame_loaded_opt_label.grid(row=0, column=0, sticky="nsew")
        frame_unloaded_opt_label.grid(row=0, column=1, sticky="nsew")
        frame_loaded_opt_data.grid(row=1, column=0, sticky="nsew")
        frame_unloaded_opt_data.grid(row=1, column=1, sticky="nsew")
        
        frame_thrashing_opt_data_seconds.grid(row=0, column=0, sticky="nsew")
        frame_thrashing_opt_data_percentage.grid(row=0, column=1, sticky="nsew")
        
        frame_loaded_alg_label.grid(row=0, column=0, sticky="nsew")
        frame_unloaded_alg_label.grid(row=0, column=1, sticky="nsew")
        frame_loaded_alg_data.grid(row=1, column=0, sticky="nsew")
        frame_unloaded_alg_data.grid(row=1, column=1, sticky="nsew")
        
        frame_thrashing_alg_data_seconds.grid(row=0, column=0, sticky="nsew")
        frame_thrashing_alg_data_percentage.grid(row=0, column=1, sticky="nsew")
        
        
        #Labels
        statistics_processes_opt_label = customtkinter.CTkLabel(frame_processes_opt_label, text="Processes", font=("Constantia",15), width=325)
        statistics_sim_time_opt_label = customtkinter.CTkLabel(frame_sim_time_opt_label, text="Sim-Time", font=("Constantia",15), width=325)
        statistics_ram_kb_opt_label = customtkinter.CTkLabel(frame_ram_kb_opt_label, text="RAM KB", font=("Constantia",15), width=162.5)
        statistics_ram_percentage_opt_label = customtkinter.CTkLabel(frame_ram_percentage_opt_label, text="RAM %", font=("Constantia",15), width=162.5)
        statistics_v_ram_kb_opt_label = customtkinter.CTkLabel(frame_v_ram_kb_opt_label, text="V-RAM KB", font=("Constantia",15), width=162.5)
        statistics_v_ram_percentage_opt_label = customtkinter.CTkLabel(frame_v_ram_percentage_opt_label, text="V-RAM-%", font=("Constantia",15), width=162.5)
        statistics_pages_opt_label = customtkinter.CTkLabel(frame_pages_opt_label, text="PAGES", font=("Constantia",15), width=325)
        statistics_loaded_opt_label = customtkinter.CTkLabel(frame_loaded_opt_label, text="LOADED", font=("Constantia",15), width=165.5)
        statistics_unloaded_opt_label = customtkinter.CTkLabel(frame_unloaded_opt_label, text="UNLOADED", font=("Constantia",15), width=165.5)
        statistics_thrashing_opt_label = customtkinter.CTkLabel(frame_thrashing_opt_label, text="Thrashing", font=("Constantia",15), width=165.5)
        statistics_fragmentacion_opt_label = customtkinter.CTkLabel(frame_fragmentacion_opt_label, text="Fragmentacion", font=("Constantia",15), width=165.5)
        
        statistics_processes_opt_data = customtkinter.CTkLabel(frame_processes_opt_data, textvariable = processes_opt, font=("Constantia",15), width=325)
        statistics_sim_time_opt_data = customtkinter.CTkLabel(frame_sim_time_opt_data, textvariable = sim_time_opt, font=("Constantia",15), width=325)
        statistics_ram_kb_opt_data = customtkinter.CTkLabel(frame_ram_kb_opt_data, textvariable=ram_kb_opt, font=("Constantia",15), width=162.5)
        statistics_ram_percentage_opt_data = customtkinter.CTkLabel(frame_ram_percentage_opt_data, textvariable= ram_percentage_opt, font=("Constantia",15), width=162.5)
        statistics_v_ram_kb_opt_data = customtkinter.CTkLabel(frame_v_ram_kb_opt_data, textvariable = v_ram_kb_opt, font=("Constantia",15), width=162.5)
        statistics_v_ram_percentage_opt_data = customtkinter.CTkLabel(frame_v_ram_percentage_opt_data, textvariable = v_ram_percentage_opt, font=("Constantia",15), width=162.5)
        statistics_loaded_opt_data = customtkinter.CTkLabel(frame_loaded_opt_data, textvariable= loaded_pages_opt, font=("Constantia",15), width=162.5)
        statistics_unloaded_opt_data = customtkinter.CTkLabel(frame_unloaded_opt_data, textvariable = unloaded_pages_opt, font=("Constantia",15), width=162.5)
        statistics_thrashing_opt_data_seconds = customtkinter.CTkLabel(frame_thrashing_opt_data_seconds, textvariable= seconds_thrashing_opt, font=("Constantia",15), width=81.25, height=50)
        statistics_thrashing_opt_data_percentage = customtkinter.CTkLabel(frame_thrashing_opt_data_percentage, textvariable= percentage_thrashing_opt, font=("Constantia",15), width=81.25, height=50)
        statistics_fragmentacion_opt_data = customtkinter.CTkLabel(frame_fragmentacion_opt_data, textvariable = fragmentacion_opt, font=("Constantia",15), width= 162.5, height=50)
        
        #
        
        statistics_processes_alg_label = customtkinter.CTkLabel(frame_processes_alg_label, text="Processess", font=("Constantia",15), width=325)
        statistics_sim_time_alg_label = customtkinter.CTkLabel(frame_sim_time_alg_label, text="Sim-Time", font=("Constantia",15), width=325)
        statistics_ram_kb_alg_label = customtkinter.CTkLabel(frame_ram_kb_alg_label, text="RAM KB", font=("Constantia",15), width=162.5)
        statistics_ram_percentage_alg_label = customtkinter.CTkLabel(frame_ram_percentage_alg_label, text="RAM %", font=("Constantia",15), width=162.5)
        statistics_v_ram_kb_alg_label = customtkinter.CTkLabel(frame_v_ram_kb_alg_label, text="V-RAM KB", font=("Constantia",15), width=162.5)
        statistics_v_ram_percentage_alg_label = customtkinter.CTkLabel(frame_v_ram_percentage_alg_label, text="V-RAM-%", font=("Constantia",15), width=162.5)
        statistics_pages_alg_label = customtkinter.CTkLabel(frame_pages_alg_label, text="PAGES", font=("Constantia",15), width=325)
        statistics_loaded_alg_label = customtkinter.CTkLabel(frame_loaded_alg_label, text="LOADED", font=("Constantia",15), width=165.5)
        statistics_unloaded_alg_label = customtkinter.CTkLabel(frame_unloaded_alg_label, text="UNLOADED", font=("Constantia",15), width=165.5)
        statistics_thrashing_alg_label = customtkinter.CTkLabel(frame_thrashing_alg_label, text="Thrashing", font=("Constantia",15), width=165.5)
        statistics_fragmentacion_alg_label = customtkinter.CTkLabel(frame_fragmentacion_alg_label, text="Fragmentacion", font=("Constantia",15), width=165.5)
        
        statistics_processes_alg_data = customtkinter.CTkLabel(frame_processes_alg_data, textvariable= processes_alg, font=("Constantia",15), width=325)
        statistics_sim_time_alg_data = customtkinter.CTkLabel(frame_sim_time_alg_data, textvariable = sim_time_alg, font=("Constantia",15), width=325)
        statistics_ram_kb_alg_data = customtkinter.CTkLabel(frame_ram_kb_alg_data, textvariable = ram_kb_alg, font=("Constantia",15), width=162.5)
        statistics_ram_percentage_alg_data = customtkinter.CTkLabel(frame_ram_percentage_alg_data, textvariable = ram_percentage_alg, font=("Constantia",15), width=162.5)
        statistics_v_ram_kb_alg_data = customtkinter.CTkLabel(frame_v_ram_kb_alg_data, textvariable= v_ram_kb_alg, font=("Constantia",15), width=162.5)
        statistics_v_ram_percentage_alg_data = customtkinter.CTkLabel(frame_v_ram_percentage_alg_data, textvariable= v_ram_percentage_alg, font=("Constantia",15), width=162.5)
        statistics_loaded_alg_data = customtkinter.CTkLabel(frame_loaded_alg_data, textvariable= loaded_pages_alg, font=("Constantia",15), width=162.5)
        statistics_unloaded_alg_data = customtkinter.CTkLabel(frame_unloaded_alg_data, textvariable= unloaded_pages_alg, font=("Constantia",15), width=162.5)
        statistics_thrashing_alg_data_seconds = customtkinter.CTkLabel(frame_thrashing_alg_data_seconds, textvariable= seconds_thrashing_alg , font=("Constantia",15), width=81.25, height=50)
        statistics_thrashing_alg_data_percentage = customtkinter.CTkLabel(frame_thrashing_alg_data_percentage, textvariable = percentage_thrashing_alg, font=("Constantia",15), width=81.25, height=50)
        statistics_fragmentacion_alg_data = customtkinter.CTkLabel(frame_fragmentacion_alg_data, textvariable = fragmentacion_alg, font=("Constantia",15), width= 162.5, height=50)
        
        #Place
        statistics_processes_opt_label.place(x = 0, y = 0)
        statistics_sim_time_opt_label.place(x = 0, y = 0)
        statistics_ram_kb_opt_label.place(x = 0, y = 0)
        statistics_ram_percentage_opt_label.place(x = 0, y = 0)
        statistics_v_ram_kb_opt_label.place(x = 0, y = 0)
        statistics_v_ram_percentage_opt_label.place(x = 0, y = 0)
        
        statistics_pages_opt_label.place(x = 0, y = 0)
        statistics_loaded_opt_label.place(x = 0, y = 0)
        statistics_unloaded_opt_label.place(x = 0, y = 0)
        statistics_thrashing_opt_label.place(x = 0, y = 0)
        statistics_fragmentacion_opt_label.place(x = 0, y = 0)
        
        statistics_processes_opt_data.place(x = 0, y = 0)
        statistics_sim_time_opt_data.place(x = 0, y = 0)
        statistics_ram_kb_opt_data.place(x = 0, y = 0)
        statistics_ram_percentage_opt_data.place(x = 0, y = 0)
        statistics_v_ram_kb_opt_data.place(x = 0, y = 0)
        statistics_v_ram_percentage_opt_data.place(x = 0, y = 0)
        
        statistics_loaded_opt_data.place(x = 0, y = 0)
        statistics_unloaded_opt_data.place(x = 0, y = 0)
        statistics_thrashing_opt_data_seconds.place(x = 0, y = 0)
        statistics_thrashing_opt_data_percentage.place(x = 0, y = 0)
        statistics_fragmentacion_opt_data.place(x = 0, y = 0)
        
        #
        
        statistics_processes_alg_label.place(x = 0, y = 0)
        statistics_sim_time_alg_label.place(x = 0, y = 0)
        statistics_ram_kb_alg_label.place(x = 0, y = 0)
        statistics_ram_percentage_alg_label.place(x = 0, y = 0)
        statistics_v_ram_kb_alg_label.place(x = 0, y = 0)
        statistics_v_ram_percentage_alg_label.place(x = 0, y = 0)
        
        statistics_pages_alg_label.place(x = 0, y = 0)
        statistics_loaded_alg_label.place(x = 0, y = 0)
        statistics_unloaded_alg_label.place(x = 0, y = 0)
        statistics_thrashing_alg_label.place(x = 0, y = 0)
        statistics_fragmentacion_alg_label.place(x = 0, y = 0)
        
        statistics_processes_alg_data.place(x = 0, y = 0)
        statistics_sim_time_alg_data.place(x = 0, y = 0)
        statistics_ram_kb_alg_data.place(x = 0, y = 0)
        statistics_ram_percentage_alg_data.place(x = 0, y = 0)
        statistics_v_ram_kb_alg_data.place(x = 0, y = 0)
        statistics_v_ram_percentage_alg_data.place(x = 0, y = 0)
        
        statistics_loaded_alg_data.place(x = 0, y = 0)
        statistics_unloaded_alg_data.place(x = 0, y = 0)
        statistics_thrashing_alg_data_seconds.place(x = 0, y = 0)
        statistics_thrashing_alg_data_percentage.place(x = 0, y = 0)
        statistics_fragmentacion_alg_data.place(x = 0, y = 0)
        
        
        
        
        #Table configure
        
        section_data_opt_statistics.grid_rowconfigure(0, weight=1)
        section_data_opt_statistics.grid_columnconfigure((0,1), weight=1)
        
        frame_processes_opt_label.grid(row = 0, column = 0, columnspan = 2, sticky="nsew")
        frame_sim_time_opt_label.grid(row = 0, column = 2, columnspan = 2, sticky="nsew")
        frame_ram_kb_opt_label.grid(row = 2, column = 0, sticky="nsew")
        frame_ram_percentage_opt_label.grid(row = 2, column = 1, sticky="nsew")
        frame_v_ram_kb_opt_label.grid(row = 2, column = 2, sticky="nsew")
        frame_v_ram_percentage_opt_label.grid(row = 2, column = 3, sticky="nsew")
        frame_pages_opt_label.grid(row = 4, column = 0,columnspan=2, sticky="nsew")
        frame_thrashing_opt_label.grid(row = 4, column = 2, sticky="nsew")
        frame_fragmentacion_opt_label.grid(row = 4, column = 3, sticky="nsew")
        
        frame_processes_opt_data.grid(row = 1, column = 0, columnspan = 2, sticky="nsew")
        frame_sim_time_opt_data.grid(row = 1, column = 2, columnspan = 2, sticky="nsew")
        frame_ram_kb_opt_data.grid(row = 3, column = 0, sticky="nsew")
        frame_ram_percentage_opt_data.grid(row = 3, column = 1, sticky="nsew")
        frame_v_ram_kb_opt_data.grid(row = 3, column = 2, sticky="nsew")
        frame_v_ram_percentage_opt_data.grid(row = 3, column = 3, sticky="nsew")
        frame_pages_child_opt_label.grid(row = 5, column = 0,rowspan=2 , columnspan = 2, sticky="nsew")
        frame_thrashing_opt_data.grid(row=5, column=2, rowspan=2, sticky="nsew")
        frame_fragmentacion_opt_data.grid(row=5, column=3, rowspan=2, sticky="nsew")
        
        #
        
        section_data_alg_statistics.grid_rowconfigure(0, weight=1)
        section_data_alg_statistics.grid_columnconfigure((0,1), weight=1)
        
        frame_processes_alg_label.grid(row = 0, column = 0, columnspan = 2, sticky="nsew")
        frame_sim_time_alg_label.grid(row = 0, column = 2, columnspan = 2, sticky="nsew")
        frame_ram_kb_alg_label.grid(row = 2, column = 0, sticky="nsew")
        frame_ram_percentage_alg_label.grid(row = 2, column = 1, sticky="nsew")
        frame_v_ram_kb_alg_label.grid(row = 2, column = 2, sticky="nsew")
        frame_v_ram_percentage_alg_label.grid(row = 2, column = 3, sticky="nsew")
        frame_pages_alg_label.grid(row = 4, column = 0,columnspan=2, sticky="nsew")
        frame_thrashing_alg_label.grid(row = 4, column = 2, sticky="nsew")
        frame_fragmentacion_alg_label.grid(row = 4, column = 3, sticky="nsew")
        
        frame_processes_alg_data.grid(row = 1, column = 0, columnspan = 2, sticky="nsew")
        frame_sim_time_alg_data.grid(row = 1, column = 2, columnspan = 2, sticky="nsew")
        frame_ram_kb_alg_data.grid(row = 3, column = 0, sticky="nsew")
        frame_ram_percentage_alg_data.grid(row = 3, column = 1, sticky="nsew")
        frame_v_ram_kb_alg_data.grid(row = 3, column = 2, sticky="nsew")
        frame_v_ram_percentage_alg_data.grid(row = 3, column = 3, sticky="nsew")
        frame_pages_child_alg_label.grid(row = 5, column = 0,rowspan=2 , columnspan = 2, sticky="nsew")
        frame_thrashing_alg_data.grid(row=5, column=2, rowspan=2, sticky="nsew")
        frame_fragmentacion_alg_data.grid(row=5, column=3, rowspan=2, sticky="nsew")
            
              

# Ejecutar el bucle principal
main_proyect(window)
window.mainloop()
