# GUI_Clock

This program defines a `Clock` class with methods to implement a timer and countdown. It uses the `customtkinter` and `tkinter` modules to create a GUI that displays the current time, weekday, and date, and provides buttons to start and stop the timer and countdown, as well as an entry for selecting the file path for the timer.

## Dependencies
* `customtkinter`
* `tkinter`
* `time`
* `filedialog`

## How to Run the Program
To run the program, execute the following command:

```
python gui_clock.py
```

## Program Description
The program initializes a `Clock` object and creates a GUI using the `customtkinter` module. The GUI displays the current time, weekday, and date, and provides buttons to start and stop the timer and countdown. The program uses the `time` module to get the current time and date, and the `filedialog` module to allow the user to select the file path for the timer.

### Timer
The program implements a timer using the `time` module. The user can select the file path for the timer, and the program will write the elapsed time to the file when the timer is stopped.

### Countdown
The program implements a countdown using the `time` module. The user can enter the duration of the countdown in minutes and seconds, and the program will display the remaining time in the GUI.

## Usage
To start the timer, click the "Start timer" button. To stop the timer, click the "Stop timer" button. To start the countdown, enter the duration of the countdown in the "Min" and "Sec" fields and click the "Start countdown" button. To stop the countdown, click the "Stop countdown" button.
