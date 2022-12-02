import tkinter as tk
import os
from mentorPreference.index import StartPage
from mentorPreference.mm import MentorMenu
from mentors.mm import MentorsModel


class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # When the program is started
        # StartPage handles the initial
        # menu displayed
        self.is_authenticated = False
        self.credentials = dict()
        script_dir = os.path.abspath( os.path.dirname( __file__ ) )
        self.db_path = script_dir + "\mentor_network.db"
        self.mentor_model = MentorsModel(r"" + self.db_path)
        self.frame = StartPage(self)

    def submit_login(self, id, first_name, last_name):
        record = self.mentor_model.select_by_id_and_name(id.get(), first_name.get(), last_name.get())

        if len(record) == 1: # if the record is found, proceed to the menu
            self.set_credentials(record[0])
            self.set_authenticated(True)
            self.show_frame('MentorMenu')
        else:
            print('invalid credentials')
            tk.Label(self, text='Invalid credentials, please try again', font=10).pack()

    def show_frame(self, class_name):
        """ Displays requested menu based on authenticated status


        If a user is not authenticated, the display defaults to the StartPage.
        Otherwise a requested menu is displayed
        -------------------
        Parameters
            class_name (string): Name of a class that contains the logic for 
            constructing a requested menu
        """
        if self.is_authenticated == False: # if a user is authenticated display StartPage
            self.frame.destroy()
            self.frame = eval('StartPage')(self)
        else:
            self.frame.destroy()
            self.frame = eval(class_name)(self)

    def set_authenticated(self, bol_value):
        """Sets is_authenticated property to a passed boolean value

        ----------------
        Parameters:
            bol_value: boolean
        """
        self.is_authenticated = bol_value

    def set_credentials(self, credentials):
        self.credentials = credentials

    def get_db_path(self):
        """Returns value of db_path property

        Returns the path the database
        """
        return self.db_path

# Driver Code
app = tkinterApp()
app.mainloop()