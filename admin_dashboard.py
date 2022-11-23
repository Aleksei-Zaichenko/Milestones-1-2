import tkinter as tk
from tkinter import ttk
import os
from organizations.oc import OrganizationsController
from mentors.index import Mentors
from programs.index import TrainingProgram
from startMenu.sp import StartPage

LARGEFONT = ("Verdana", 35)
  
class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # When the program is started
        # StartPage handles the initial 
        # menu displayed
        self.frame = StartPage(self)
        script_dir = os.path.abspath( os.path.dirname( __file__ ) )
        self.db_path = script_dir + "\mentor_network.db"

    # display requested page
    def show_frame(self, class_name):
        self.frame.destroy()
        self.frame = eval(class_name)(self)

    def get_db_path(self):
        return self.db_path

class Organizations(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side = "top", fill = "both", expand = True)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.controller = OrganizationsController(parent.get_db_path())
        self.parent_controller = parent
        self.container = self.get_initial_frame(self)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        self.container.destroy()
        if cont == 'initial':
            self.container = self.get_initial_frame(self)
        if cont == 'add':
            self.container = self.get_add_frame(self)
        if cont == 'delete':
            self.container = self.get_delete_frame(self)
        if cont == 'modify':
            self.container = self.get_modify_frame(self)

    def get_initial_frame(self, parent):
        frame = tk.Frame(master=parent)
        frame.grid(row = 0, column = 0)
  
        frame.grid_rowconfigure(0, weight = 1)
        frame.grid_columnconfigure(0, weight = 1)

        label = ttk.Label(frame, text="Organizations Menu", font = LARGEFONT)
        label.grid(row = 0, column = 0)

        menu_frame = tk.Label(frame)
        menu_frame.grid(row = 1, column = 0)

        button1 = ttk.Button(menu_frame, text ="Add", command = lambda : self.show_frame('add'))
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        button2 = ttk.Button(menu_frame, text ="modify", command = lambda : self.show_frame('modify'))
        button2.grid(row = 1, column = 2, padx = 10, pady = 10)

        button3 = ttk.Button(menu_frame, text ="Delete", command = lambda : self.show_frame('delete'))
        button3.grid(row = 1, column = 3, padx = 10, pady = 10)

        back_button = ttk.Button(menu_frame, text ="Back", command = lambda : self.parent_controller.show_frame(StartPage))
        back_button.grid(row = 2, column = 2, padx = 10, pady = 10)

        return frame

    def get_add_frame(self,parent):
        row_value = 0

        frame = tk.Frame(master=parent)
        frame.grid(row = 0, column = 0)
  
        frame.grid_rowconfigure(0, weight = 1)
        frame.grid_columnconfigure(0, weight = 1)

        label = ttk.Label(frame, text ="Add Menu", font = LARGEFONT)
        label.grid(row = row_value, column = 0)
        row_value += 1

        records_frame = ttk.LabelFrame(frame)
        records_frame.grid(row = 1, column = 0, sticky="NSEW")

        self.controller.construct_add_frame(records_frame)
        row_value += 1

        back_button = ttk.Button(frame, text ="Back", command = lambda : self.show_frame('initial'))
        back_button.grid(row = row_value, column = 0)
        return frame

    def get_delete_frame(self, parent):
        frame = tk.Frame(master=parent)
        frame.pack(side = "top", fill = "both", expand = True)
  
        frame.grid_rowconfigure(0, weight = 1)
        frame.grid_rowconfigure(1, weight = 1)
        frame.grid_columnconfigure(0, weight = 1)

        label = ttk.Label(frame, text = "Delete Menu", font = LARGEFONT)
        label.grid(row = 0, column = 0)

        records_frame = ttk.LabelFrame(frame)
        records_frame.grid(row = 1, column = 0, sticky="NSEW")
        records_frame.grid_columnconfigure(0, weight = 1)

        self.controller.construct_delete_frame(records_frame)

        back_button = ttk.Button(frame, text ="Back", command = lambda : self.show_frame('initial'))
        back_button.grid(row = 2, column = 0)
        return frame

    def get_modify_frame(self, parent):
        row_value = 0

        frame = tk.Frame(master=parent)
        frame.pack(side = "top", fill = "both", expand = True)
  
        frame.grid_rowconfigure(0, weight = 1)
        frame.grid_columnconfigure(0, weight = 1)

        label = ttk.Label(frame, text ="Modify Menu", font = LARGEFONT)
        label.grid(row = row_value, column = 0)
        row_value += 1

        records_frame = ttk.LabelFrame(frame)
        records_frame.grid(row = row_value, column = 0, sticky="NSEW")
        row_value += 1

        self.controller.construct_modify_frame(records_frame)

        back_button = ttk.Button(frame, text ="Back", command = lambda : self.show_frame('initial'))
        back_button.grid(row = row_value, column = 0)
        return frame

# second window frame Courses
class Courses(tk.Frame):
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="p1", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Organizations",
                            command = lambda : controller.show_frame(Organizations))
     
        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text ="Page 2",
                            command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

# Driver Code
app = tkinterApp()
app.mainloop()
