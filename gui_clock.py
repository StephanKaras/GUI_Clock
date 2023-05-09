'''
▶ Write a graphical user interface (GUI) for a clock. 
▶ The clock should graphically display the current time (hour, minute, seconds), day of week (e.g. Friday) and date (e.g. 01. Mai 2023). This display should be readable and nicely formated other than that, you may choose the display mode freely (e.g. write date as 2023-05-01).
▶ The GUI contains a button that starts a timer (e.g. has a label Start timer or something similar). After the timer has started, the button changes its labeling (e.g. to Stop timer). When the timer is stopped, the start time, end time and duration are written to a file.
▶ The timer file is created if nonexistent, otherwise new timings
   are always added to the end of it.

▶ There is an editable text field to define the location of the timer file. A button goes along with it that opens a file selection dialog and stores the resulting path in the editable field. The timer file is always defined by the editable field.
▶ In addition, there are 2 text fields for setting a minute and seconds countdown. There is a Countdown button that starts the countdown. After the countdown, a message is presented to the user informing them that the countdown has ended. The countdown is updated live in the text fields.
▶ Timer and countdown can be used simultaneously.

▶ There are labels for the countdown text fields that mark them as minutes and seconds.
▶ The timer button may not only change its text when started, but
   can also change its color.
'''

'''
pip install customtkinter


'''

import time
import customtkinter as tk
from tkinter import filedialog

class Clock:

    def __init__(self):
        self.time = time.localtime() # the current time as a time object
        # weekday as a string
        self.weekday = time.strftime('%A', self.time) # the weekday as a string: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
        self.date = f'{self.time.tm_mday}-{self.time.tm_mon}-{self.time.tm_year}' # the date in the format: 01-05-2023
        self.current_time = f'{self.time.tm_hour}:{self.time.tm_min}:{self.time.tm_sec}' # the time in the format: 12:30:15

        # timer variables
        self.timer_running = False
        self.timer_start_time = None
        self.timer_end_time = None
        self.timer_duration = None

        # countdown variables
        self.countdown_running = False
        self.countdown_start_time = None
        self.countdown_end_time = None
        self.countdown_duration = None

        # Widgets
        self.label = tk.CTkLabel(frame, text=str(self.current_time), font=("", 40)) # time label
        self.label.pack(pady=10, padx=10) 

        self.weekday_label = tk.CTkLabel(frame, text=str(self.weekday), font=("", 20)) # weekday label
        self.weekday_label.pack(pady=0, padx=10)

        self.date_label = tk.CTkLabel(frame, text=str(self.date), font=("", 20)) # date label
        self.date_label.pack(pady=5, padx=10)
        
        # timer widgets
        # timer button, will start the timer when clicked and change its text to 'Stop timer'. When clicked again, it will stop the timer and change its text back to 'Start timer'
        self.timer_button = tk.CTkButton(frame, text='Start timer', command=self.toggle_timer) # timer button
        self.timer_button.pack(pady=12, padx=10)

        self.update() # update the time every second


    def update(self):
        self.time = time.localtime()
        self.weekday = self.time.tm_wday
        self.date = f'{self.time.tm_mday}-{self.time.tm_mon}-{self.time.tm_year}'
        self.current_time = f'{self.time.tm_hour}:{self.time.tm_min}:{self.time.tm_sec}'
        self.label.configure(text=str(self.current_time)) # update the time label
        root.after(1000, self.update) # update the time every second
    
    # implementation of the timer
        
    def toggle_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_start_time = time.localtime()
            print('timer started')
            self.timer_button.configure(text="Stop timer")
        else: 
            self.timer_running = False
            self.timer_end_time = time.localtime()
            self.timer_duration = time.mktime(self.timer_end_time) - time.mktime(self.timer_start_time)

            def select_file():
                file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
                return str(file_path)
            
            path = select_file()
            self.write_timer(path)
            print('timer stopped')  
            self.timer_button.configure(text="Start timer")     

    def write_timer(self, path):
        if self.timer_running == False:
            with open(path, 'a') as f:
                f.write(f'{self.timer_start_time.tm_hour}:{self.timer_start_time.tm_min}:{self.timer_start_time.tm_sec} - {self.timer_end_time.tm_hour}:{self.timer_end_time.tm_min}:{self.timer_end_time.tm_sec} - {self.timer_duration}\n')
            print('timer written to file')
            return True
        else:
            print('timer still running')
            return False



# GUI setup

tk.set_appearance_mode('dark') # light or dark
tk.set_default_color_theme('dark-blue')

# main window
root = tk.CTk()
root.geometry('500x300') 

# main frame
frame = tk.CTkFrame(root)
frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

clock = Clock() # create a clock object

root.mainloop() # run the main loop
