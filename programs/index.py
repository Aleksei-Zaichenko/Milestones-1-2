from datetime import datetime
from time import mktime
import tkinter as tk
from tkinter import ttk
from programs.tpm import TrainingProgramModel
from organizations.om import OrganizationsModel
import programs.fonts

class TrainingProgram(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(side = "top", fill = "both", expand = True)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.parent_controller = parent
        self.model = TrainingProgramModel(r"" + parent.get_db_path())
        self.org_model = OrganizationsModel(r"" + parent.get_db_path())
        self.container = self.get_initial_frame(self)

    def get_initial_frame(self, parent_frame):
        time_types = [
        "AM",
        "PM",
        ]

        head_frame = tk.Frame(parent_frame)
        head_frame.pack(pady=10)
        head_frame.pack_propagate(False)
        head_frame.configure(width=400, height=490)

        heading_lb = tk.Label(head_frame, text='Programs and Courses Registration System',
                     font=programs.fonts.main,
                     bg='pink')
        heading_lb.pack(fill=tk.X, pady=5)

        course_id_lb = tk.Label(head_frame, text='Course ID:', font=programs.fonts.sub)
        course_id_lb.place(x=0, y=40)
        course_id_entry = tk.Entry(head_frame, font=programs.fonts.sub)
        course_id_entry.place(x=110, y=40, width=180)

        course_name_lb = tk.Label(head_frame, text='Course Name:', font=programs.fonts.sub)
        course_name_lb.place(x=0, y=80)
        course_name_entry = tk.Entry(head_frame, font=programs.fonts.sub)
        course_name_entry.place(x=110, y=80, width=180)

        subject_area_lb = tk.Label(head_frame, text='Subject Area:', font=programs.fonts.sub)
        subject_area_lb.place(x=0, y=120)
        subject_area_entry = tk.Entry(head_frame, font=programs.fonts.sub)
        subject_area_entry.place(x=110, y=120, width=180)


        # Drop down menu to choose an university or organization
        # --------------------------------------------------------------------------------    
        organizations = self.org_model.select_all()
        organizations_lb = tk.Label(head_frame, text='Organization:', font=programs.fonts.sub)
        organizations_lb.place(x=0, y=160)
        options = [
        "Choose an organization",
        ]

        for organization in organizations:
            options.append(organization[1])

        op_menu_value = tk.StringVar()
        op_menu_value.set(options[0]) # default value
        w = tk.OptionMenu(head_frame, op_menu_value, *options)
        w.place(x=110, y=160, width=180)
        # --------------------------------------------------------------------------------   


        start_date_lb = tk.Label(head_frame, text='Start Date:', font=programs.fonts.sub)
        start_date_lb.place(x=0, y=200)

        start_date_entry = tk.Entry(head_frame, font=programs.fonts.sub)
        start_date_entry.place(x=110, y=200, width=180)

        end_date_lb = tk.Label(head_frame, text='End Date:', font=programs.fonts.sub)
        end_date_lb.place(x=0, y=250)

        end_date_entry = tk.Entry(head_frame, font=programs.fonts.sub)
        end_date_entry.place(x=110, y=250, width=180)

        start_time_lb = tk.Label(head_frame, text='Start Time(e.g 10:45):', font=programs.fonts.sub)
        start_time_lb.place(x=0, y=300)
        start_time_entry = tk.Entry(head_frame, font=programs.fonts.sub)
        start_time_entry.place(x=130, y=300, width=100)
        start_time_type = tk.StringVar()
        start_time_type.set(time_types[0]) # default value
        start_time_ops = tk.OptionMenu(head_frame, start_time_type, *time_types)
        start_time_ops.place(x=230, y=300, width=60)

        end_time_lb = tk.Label(head_frame, text='End Time(e.g 11:45):', font=programs.fonts.sub)
        end_time_lb.place(x=0, y=350)
        end_time_entry = tk.Entry(head_frame, font=programs.fonts.sub)
        end_time_entry.place(x=130, y=350, width=100)
        end_time_type = tk.StringVar()
        end_time_type.set(time_types[0]) # default value
        end_time_ops = tk.OptionMenu(head_frame, end_time_type, *time_types)
        end_time_ops.place(x=230, y=350, width=60)

        #______________________________Buttons____________________________________________________
        register_btn = tk.Button(head_frame, text='Register', font=programs.fonts.mid,
                                command=lambda: self.add_program(record_table, [course_id_entry, course_name_entry, 
                                                                subject_area_entry, start_date_entry, end_date_entry,
                                                                start_time_entry, end_time_entry],
                                                                [start_time_type, end_time_type], op_menu_value))
        register_btn.place(x=0, y=400)

        update_btn = tk.Button(head_frame, text='Update', font=programs.fonts.mid,
                            command=lambda: self.update_program(record_table, course_id_entry, course_name_entry, 
                                                                subject_area_entry, start_date_entry, end_date_entry,
                                                                start_time_entry, end_time_entry, 
                                                                start_time_type, end_time_type, op_menu_value))
        update_btn.place(x=85, y=400)

        delete_btn = tk.Button(head_frame, text='Delete', font=programs.fonts.mid,
                            command=lambda: self.delete_program(record_table, [course_id_entry, course_name_entry, 
                                                                subject_area_entry, start_date_entry, end_date_entry,
                                                                start_time_entry, end_time_entry],
                                                                start_time_type, end_time_type, op_menu_value))
        delete_btn.place(x=160, y=400)

        clear_btn = tk.Button(head_frame, text='Clear', font=programs.fonts.mid,
                            command=lambda: self.clear_inputs([course_id_entry, course_name_entry, 
                                                                subject_area_entry, start_date_entry, end_date_entry,
                                                                start_time_entry, end_time_entry],
                                                                start_time_type, end_time_type, op_menu_value)
                            )
        clear_btn.place(x=230, y=400)

        back_btn = tk.Button(head_frame, text ="Back", font=programs.fonts.mid,
                            command = lambda : self.parent_controller.show_frame('StartPage'))
        back_btn.place(x=230, y=440)
        #________________________________Buttons____________________________________________________


        # Search Section --------------------------------------------------------------------------
        search_bar_frame = tk.Frame(parent_frame)
        search_bar_frame.pack(pady=0)
        search_bar_frame.pack_propagate(False)
        search_bar_frame.configure(width=450, height=120)

        search_lb = tk.Label(search_bar_frame,
                            text='Search a course/program for a given time window',
                            font=programs.fonts.sub)
        search_lb.pack(anchor=tk.W)
        search_from_lb = tk.Label(search_bar_frame, text='From:', font=programs.fonts.sub)
        search_from_lb.pack(anchor=tk.W)
        # search_from_lb.place(x=0, y=20)
        search_start_time = tk.Entry(search_bar_frame, font=programs.fonts.sub)
        search_start_time.place(x=50, y=25, width=50)

        from_meridiem = tk.StringVar()
        from_meridiem.set(time_types[0]) # default value
        from_ops = tk.OptionMenu(search_bar_frame, from_meridiem, *time_types)
        from_ops.place(x=110, y=25, width=60)
        search_start_time.bind('<KeyRelease>', lambda e: self.find_program_by_time(record_table, 
                                                                                    search_start_time.get(),
                                                                                    from_meridiem.get(),
                                                                                    search_end_time.get(),
                                                                                    to_meridiem.get()
                                                                                    ))

        search_to_lb = tk.Label(search_bar_frame, text='To:', font=programs.fonts.sub)
        search_to_lb.pack(anchor=tk.W)
        search_end_time = tk.Entry(search_bar_frame, font=programs.fonts.sub)
        search_end_time.place(x=50, y=50, width=50)
        to_meridiem = tk.StringVar()
        to_meridiem.set(time_types[1]) # default value
        to_ops = tk.OptionMenu(search_bar_frame, to_meridiem, *time_types)
        to_ops.place(x=110, y=50, width=60)
        search_end_time.bind('<KeyRelease>', lambda e: self.find_program_by_time(record_table, 
                                                                                search_start_time.get(),
                                                                                from_meridiem.get(),
                                                                                search_end_time.get(),
                                                                                to_meridiem.get()
                                                                                ))


        search_lb = tk.Label(search_bar_frame,
                            text='Search a course/program for a specified university or training organization',
                            font=programs.fonts.sub)
        search_lb.pack(anchor=tk.W, pady=5)
        search_by_org_entry = tk.Entry(search_bar_frame, font=programs.fonts.sub)
        search_by_org_entry.pack(anchor=tk.W)
        search_by_org_entry.bind('<KeyRelease>', lambda e: self.find_program_by_org(record_table, search_by_org_entry.get()))
        # Search Section End --------------------------------------------------------------------------


        record_frame = tk.Frame(parent_frame)
        record_frame.pack(pady=10)
        record_frame.pack_propagate(False)
        record_frame.configure(width=900, height=700)

        record_lb = tk.Label(record_frame, text= 'Select Record for Delete or Update',
                            bg='pink', font=programs.fonts.main)
        record_lb.pack(fill=tk.X)

        record_table = ttk.Treeview(record_frame)
        record_table.pack(fill=tk.X, pady=5)
                            
        #New___________________________________________________________________
        record_table.bind('<ButtonRelease-1>', lambda e: self.put_into_entries(record_table, course_id_entry, course_name_entry, 
                                                                            subject_area_entry, start_date_entry, end_date_entry,
                                                                            start_time_entry, end_time_entry, start_time_type,
                                                                            end_time_type, op_menu_value))
        #______________________________________________________________________

        record_table['column'] = ['ID', 'Course ID', 'Course Name', 'Subject Area', 'Organization Name', 
                                'Start Date', 'End Date', 'Start Time', 'End Time']

        record_table.heading('ID', text='ID', anchor=tk.W)
        record_table.heading('Course ID', text='Course ID', anchor=tk.W)
        record_table.heading('Course Name', text='Course Name', anchor=tk.W)
        record_table.heading('Subject Area', text='Subject Area', anchor=tk.W)
        record_table.heading('Organization Name', text='Organization Name', anchor=tk.W)
        record_table.heading('Start Date', text='Start Date', anchor=tk.W)
        record_table.heading('End Date', text='End Date', anchor=tk.W)
        record_table.heading('Start Time', text='Start Time', anchor=tk.W)
        record_table.heading('End Time', text='Start Time', anchor=tk.W)

        record_table.column('#0', anchor=tk.W, width=0, stretch=tk.NO)
        record_table.column('ID', anchor=tk.W, width=20)
        record_table.column('Course ID', anchor=tk.W, width=60)
        record_table.column('Course Name', anchor=tk.W, width=150)
        record_table.column('Subject Area', anchor=tk.W, width=150)
        record_table.column('Organization Name', anchor=tk.W, width=150)
        record_table.column('Start Date', anchor=tk.W, width=100)
        record_table.column('End Date', anchor=tk.W, width=100)
        record_table.column('Start Time', anchor=tk.W, width=100)
        record_table.column('End Time', anchor=tk.W, width=100)

        self.load_data(record_table)

        return head_frame

    def load_data(self, record_table):
        programs = self.model.select_all()
        self.populate_record_table(record_table, programs)

    def put_into_entries(self, record_table, course_id_entry, course_name_entry,
                        subject_area_entry, start_date_entry, end_date_entry,
                        start_time_entry, end_time_entry, start_time_type,
                        end_time_type, op_menu_value):
        curItem = record_table.focus()
        values = record_table.item(curItem)['values']
        program_id = values[0]

        program = self.model.select_program_by_id(program_id)[0]
        print(program)

        course_id_entry.delete(0, tk.END)
        course_name_entry.delete(0, tk.END)
        subject_area_entry.delete(0, tk.END)
        start_date_entry.delete(0, tk.END)
        end_date_entry.delete(0, tk.END)
        start_time_entry.delete(0, tk.END)
        end_time_entry.delete(0, tk.END)

        course_id = program[1]
        course_name = program[2]
        sub_area = program[3]
        stat_date = program[4]
        end_date = program[5]
        start_time = self.format_humanreadable(program[6], False)
        start_t_type = program[7]
        end_time = self.format_humanreadable(program[8], False)
        end_t_type = program[9]
        org_name = program[-1]

        course_id_entry.insert(0, course_id)
        course_name_entry.insert(0, course_name)
        subject_area_entry.insert(0, sub_area)
        start_date_entry.insert(0, stat_date)
        end_date_entry.insert(0, end_date)
        start_time_entry.insert(0, start_time)
        start_time_type.set(start_t_type)
        end_time_entry.insert(0, end_time)
        end_time_type.set(end_t_type)
        op_menu_value.set(org_name)

    def clear_inputs(self, entries, start_time_type, end_time_type, org_option):
        for element in entries:
            element.delete(0, tk.END)
        start_time_type.set("AM")
        end_time_type.set('AM')
        org_option.set("Choose an organization")

    def add_program(self, record_table, elements, time_types, org_option):
        values = []
        organization_id = self.org_model.select_by_name(org_option.get())[0][0]

        start_time = self.format_unixtimestamp(elements[5].get(), time_types[0].get())
        end_time = self.format_unixtimestamp(elements[6].get(), time_types[1].get())

        values.append(elements[0].get())
        values.append(elements[1].get())
        values.append(elements[2].get())
        values.append(elements[3].get())
        values.append(elements[4].get())
        values.append(start_time)
        values.append(time_types[0].get())
        values.append(end_time)
        values.append(time_types[1].get())
        values.append(organization_id)
        print(values)

        id = self.model.add_trainingProgram(tuple(values))
        self.clear_inputs(elements, time_types[0], time_types[1], org_option)
        self.load_data(record_table)

    def update_program(self, record_table, course_id_entry, course_name_entry, 
                        subject_area_entry, start_date_entry, end_date_entry,
                        start_time_entry, end_time_entry, 
                        start_time_type, end_time_type, op_menu_value):
        cur_item = record_table.focus()
        program_id = record_table.item(cur_item)['values'][0]
        organization_id = self.org_model.select_by_name(op_menu_value.get())[0][0]
        start_time = self.format_unixtimestamp(start_time_entry.get(), start_time_type.get())
        end_time = self.format_unixtimestamp(end_time_entry.get(), end_time_type.get())
        values = []
        values.append(course_id_entry.get())
        values.append(course_name_entry.get())
        values.append(subject_area_entry.get())
        values.append(start_date_entry.get())
        values.append(end_date_entry.get())
        values.append(start_time)
        values.append(start_time_type.get())
        values.append(end_time)
        values.append(end_time_type.get())
        values.append(organization_id)
        values.append(program_id)

        self.model.update_trainingProgram(tuple(values))

        self.load_data(record_table)
        self.clear_inputs([course_id_entry, course_name_entry, 
                        subject_area_entry, start_date_entry, end_date_entry,
                        start_time_entry, end_time_entry], 
                        start_time_type, end_time_type, op_menu_value)

    def delete_program(self, record_table, elements, start_time_type, end_time_type, op_menu_value):
        cur_item = record_table.focus()
        values = record_table.item(cur_item)['values']
        program_id = values[0]
        print(program_id)
        self.model.delete_trainingProgram(program_id)
        self.load_data(record_table)
        self.clear_inputs(elements, start_time_type, end_time_type, op_menu_value)

    def format_unixtimestamp(self, time, time_type):
        dt = datetime.strptime(time + ' ' + time_type, "%I:%M %p")
        dt = dt.replace(1970, 1, 1)
        return int(mktime(dt.timetuple()))

    def format_humanreadable(self, timestamp, include_type = True):
        return datetime.fromtimestamp(int(timestamp)).strftime('%I:%M %p' if include_type else '%I:%M')

    def populate_record_table(self, record_table, programs):
        for item in record_table.get_children():
            record_table.delete(item)

        for r in range(len(programs)):
            program_copy = list(programs[r]).copy()
            print(program_copy)
            program_copy.pop(-2) # remove organizations id
            program_copy.pop(-4) # remove start time type
            program_copy.pop(-2) # remove end time type
            start_time = self.format_humanreadable(program_copy[-3])
            end_time = self.format_humanreadable(program_copy[-2])
            program_copy[-3] = start_time
            program_copy[-2] = end_time
            program_copy[4], program_copy[-1] = program_copy[-1], program_copy[4] # swap organization_name with start_time
            program_copy[-3], program_copy[-1] = program_copy[-1], program_copy[-3] # swap
            program_copy[-2], program_copy[-1] = program_copy[-1], program_copy[-2] # swap
            record_table.insert(parent='', index='end', text='',
                                iid=r, values=tuple(program_copy))

    def find_program_by_org(self, record_table, org_name):
        if org_name != "":
            programs = self.model.select_program_by_org_name(org_name)
            self.populate_record_table(record_table, programs)
        else:
            self.load_data(record_table)

    def find_program_by_time(self, record_table, start_time, start_type, end_time, end_type):
        if len(start_time) > 4 or len(end_time) > 4:
            start_formatted = self.format_unixtimestamp('08:00', 'AM') # 08:00AM - minimum starting time
            end_formatted = self.format_unixtimestamp('09:00', 'PM') # 09:00PM - maximum ending time
            if len(start_time) > 4: # use passed start time if entered fully - e.x. 10:45,
                start_formatted = self.format_unixtimestamp(start_time, start_type)
            if len(end_time) > 4: # use passed end time if entered fully - e.x. 10:45,
                end_formatted = self.format_unixtimestamp(end_time, end_type)
            programs = self.model.select_program_by_time(start_formatted, end_formatted)
            self.populate_record_table(record_table, programs)
        else:
            self.load_data(record_table)