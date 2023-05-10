
'''
Author: Stephan Karas
Date: 11.05.2023
Description: This program defines a Clock class with methods to implement a timer and countdown. 
It uses the customtkinter and tkinter modules to create a GUI that displays the current time, weekday,
and date, and provides buttons to start and stop the timer and countdown, as well as an entry for selecting the file path for the timer.
Dependencies: 
    - customtkinter
    - tkinter
    - time
    - filedialog
'''

import time
import customtkinter as tk
from tkinter import filedialog
import os as os

class Clock:

    def __init__(self):
        self.time = time.localtime() # the current time as a time object
        self.weekday = time.strftime('%A', self.time) # the weekday as a string: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
        self.date = f'{self.time.tm_mday}.{self.time.tm_mon}.{self.time.tm_year}' # the date in the format: 01-05-2023
        self.current_time = f'{self.time.tm_hour}:{self.time.tm_min}:{self.time.tm_sec}' # the time in the format: 12:30:15

        # timer variables
        self.timer_running = False
        self.timer_start_time = None
        self.timer_end_time = None
        self.timer_duration = None
        self.DEFAULT_TIMER_PATH = os.path.join(os.getcwd(), 'time.txt') # the default path for the timer file, which is in the same directory as the script, named time.txt
        self.CHOSEN_TIMER_PATH = self.DEFAULT_TIMER_PATH 

        # countdown variables
        self.countdown_running = False
        self.countdown_start_min = None
        self.countdown_start_sec = None
        self.repeating_every_second = None # the function that is called every second to update the countdown

        # Widgets
        self.label = tk.CTkLabel(frame, text=str(self.current_time), font=("", 40)) # time label
        self.label.pack(pady=10, padx=10) 

        self.weekday_label = tk.CTkLabel(frame, text=str(self.weekday), font=("", 20)) # weekday label
        self.weekday_label.pack(pady=0, padx=10)

        self.date_label = tk.CTkLabel(frame, text=str(self.date), font=("", 20)) # date label
        self.date_label.pack(pady=(10, 20), padx=10)
        
        # timer widgets
        self.timer_frame = tk.CTkFrame(frame) # timer frame
        self.timer_frame.pack(pady=(5, 15), padx=10) 

        self.timer_button = tk.CTkButton(self.timer_frame, text='Start timer', command=self.toggle_timer) # timer button
        self.timer_button.grid(row=1, column=0, padx=(30, 0), pady=5)

        self.timer_path_entry = tk.CTkEntry(self.timer_frame, width=480, font=("", 11), placeholder_text=self.CHOSEN_TIMER_PATH) # timer path entry
        self.timer_path_entry.bind('<KeyRelease>', lambda event: self.modify_path()) # bind the modify_path function to the entry, which updates the path variable when the user changes the path
        self.timer_path_entry.grid(row=0, column=0, padx=3, pady=5)

        self.timer_path_chooser = tk.CTkButton(self.timer_frame, text='📁', command=self.select_file, width=25) # timer path chooser button
        self.timer_path_chooser.grid(row=0, column=1, padx=0)
        

        # countdown widgets
        countdown_frame = tk.CTkFrame(frame) # countdown frame
        countdown_frame.pack(pady=5, padx=10)

        self.countdown_min_entry = tk.CTkEntry(countdown_frame, width=50, font=("", 20), placeholder_text='Min') # countdown minutes
        self.countdown_min_entry.grid(row=0, column=0, padx=5, pady=0)# center it under the timer button

        self.countdown_min_label = tk.CTkLabel(countdown_frame, text="Min", font=("", 10)) # Minute label
        self.countdown_min_label.grid(row=1, column=0, padx=0, pady=0)

        self.countdown_label = tk.CTkLabel(countdown_frame, text=':', font=("", 20)) # countdown label
        self.countdown_label.grid(row=0, column=1, padx=0, pady=5)


        self.countdown_sec_entry = tk.CTkEntry(countdown_frame, width=50, font=("", 20), placeholder_text='Sec') # countdown Seconds
        self.countdown_sec_entry.grid(row=0, column=2, padx=5, pady=0)

        self.countdown_sec_label = tk.CTkLabel(countdown_frame, text="Sec", font=("", 10)) # Second label
        self.countdown_sec_label.grid(row=1, column=2, padx=0, pady=0)

        self.countdown_button = tk.CTkButton(countdown_frame, text='Start countdown', command=self.toggle_countdown) # countdown button
        self.countdown_button.grid(row=3, column=0, columnspan=3, padx=0, pady=5)

        self.update() # update the time every second

    # update the time every second
    def update(self):
        self.time = time.localtime()
        self.weekday = self.time.tm_wday
        self.date = f'{self.time.tm_mday}.{self.time.tm_mon}.{self.time.tm_year}'
        self.current_time = f'{self.time.tm_hour}:{self.time.tm_min}:{self.time.tm_sec}'
        self.label.configure(text=str(self.current_time)) # update the time label
        root.after(1000, self.update) # update the time every second
    
    # implementation of the timer
    def toggle_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_start_time = time.localtime()
            print('timer started')
            self.timer_button.configure(text="Stop timer", fg_color='red', hover_color='#8b0000')
        else: 
            self.timer_running = False
            self.timer_end_time = time.localtime()
            self.timer_duration = time.mktime(self.timer_end_time) - time.mktime(self.timer_start_time)
            
            path = self.CHOSEN_TIMER_PATH
            self.write_timer(path)
            print('timer stopped')  
            self.timer_button.configure(text="Start timer", fg_color='#1F538D', hover_color='#204B7C') 

    # open a file dialog to select the file to write the timer to
    def select_file(self):
            file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
            self.CHOSEN_TIMER_PATH = str(file_path)
            self.timer_path_entry.configure(placeholder_text=self.CHOSEN_TIMER_PATH)
            

    # update the path variable when the user changes the path in the entry field 
    def modify_path(self):
        self.CHOSEN_TIMER_PATH = self.timer_path_entry.get()
        self.timer_path_entry.delete(0, tk.END)
        self.timer_path_entry.insert(0, self.CHOSEN_TIMER_PATH)


    # write the timer to the file
    def write_timer(self, path):
        # if path exists, append to it. If not, create it, write the header and then append to it
        if os.path.exists(path):
             with open(path, 'a') as f:
                f.write(f'{self.timer_start_time.tm_hour}:{self.timer_start_time.tm_min}:{self.timer_start_time.tm_sec} - {self.timer_end_time.tm_hour}:{self.timer_end_time.tm_min}:{self.timer_end_time.tm_sec} - {self.timer_duration}\n')
                print('file exists')
                print('timer written to file')
                return True
        else:
            with open(path, 'w') as f:
                f.write('Start time - End time - Duration\n')
                f.write(f'{self.timer_start_time.tm_hour}:{self.timer_start_time.tm_min}:{self.timer_start_time.tm_sec} - {self.timer_end_time.tm_hour}:{self.timer_end_time.tm_min}:{self.timer_end_time.tm_sec} - {self.timer_duration}\n')
                print('file created')
                print('timer written to file')
                return True
            
    # implementation of the countdown toggle
    def toggle_countdown(self):
        if not self.countdown_running:
            self.countdown_start_min = self.countdown_min_entry.get() # get the minutes from the entry field
            self.countdown_start_sec = self.countdown_sec_entry.get() # get the seconds from the entry field

            # check input validity
            if self.countdown_start_min == '' and self.countdown_start_sec == '':
                #messagebox.showerror('Error', 'Please enter a valid time')
                self.employ_error_message('Please enter a valid time')
                print('Please enter a valid time')
                return False
            
            try: # check if the input is a number and convert it to an integer if it is
                if self.countdown_start_min and self.countdown_start_min.isdigit():
                    self.countdown_start_min = int(self.countdown_start_min)
                else: 
                    self.countdown_start_min = 0

                if self.countdown_start_sec and self.countdown_start_sec.isdigit():
                    self.countdown_start_sec = int(self.countdown_start_sec)
                else:
                    self.countdown_start_sec = 0

            except ValueError:
                self.employ_error_message('Please enter a valid time')
                print('Please enter a valid time')
                return False
            
            if self.countdown_start_min < 0 or self.countdown_start_sec < 0:
                self.employ_error_message('Please enter a valid time')
                print('Please enter a valid time')
                return False
            elif self.countdown_start_min == 0 and self.countdown_start_sec == 0:
                self.employ_error_message('Please enter a valid time')
                print('Please enter a valid time')
                return False
            else:
                self.countdown_running = True
                
                # convert the minutes and seconds to integers
                self.countdown_start_min = int(self.countdown_start_min)
                self.countdown_start_sec = int(self.countdown_start_sec)

                self.countdown_button.configure(text="Stop countdown", fg_color='red', hover_color='#8b0000') # change the button text and color
                print('countdown started')
                self.countdown()
        else:
            self.countdown_running = False
            self.countdown_button.configure(text="Start countdown", fg_color='#1F538D', hover_color='#204B7C')

             # Cancel the repeating event
            if self.repeating_every_second is not None:
                root.after_cancel(self.repeating_every_second)
                self.repeating_every_second = None
            print('countdown stopped')
            
            return False
    
    # implementation of the countdown functionality
    def countdown(self):
        if self.countdown_running: # while the countdown is running
            if self.countdown_start_min == 0 and self.countdown_start_sec == 0: # if the minutes and seconds are 0, stop the countdown
                self.countdown_running = False
                self.countdown_button.configure(text="Start countdown", fg_color='#1F538D', hover_color='#204B7C')
                self.employ_error_message('Countdown stopped') # show a message box
                print('countdown stopped')
                return False
            elif self.countdown_start_sec == 0: # if the seconds are 0, decrement the minutes and set the seconds to 59
                self.countdown_start_min -= 1 
                self.countdown_start_sec = 59
            else:
                self.countdown_start_sec -= 1

            self.countdown_min_entry.delete(0, tk.END)  # delete the old value
            self.countdown_min_entry.insert(0, self.countdown_start_min)  # insert the new value
            self.countdown_sec_entry.delete(0, tk.END)  # delete the old value
            self.countdown_sec_entry.insert(0, self.countdown_start_sec)  # insert the new value
        
        self.repeating_every_second = root.after(1000, self.countdown) # call the countdown function every second

    # creates an error message window
    def employ_error_message(self, message):
        error_message = tk.CTkToplevel() # create a new window
        error_message.geometry('400x200')
        error_message.title('Error')
        error_message.attributes('-topmost', True)  # show the error message in front of the main window
        error_message.resizable(False, False)
        error_message_label = tk.CTkLabel(error_message, text=":( " + message, font=('', 12), fg_color='#8b0000')
        error_message_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)




# GUI setup

tk.set_appearance_mode('dark') # light or dark
tk.set_default_color_theme('dark-blue')

# main window
root = tk.CTk()
root.geometry('600x400') 
root.title('Clock')
root.resizable(True, True)

# main frame
frame = tk.CTkFrame(root)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

clock = Clock() # create a clock object

root.mainloop() # run the main loop
