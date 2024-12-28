import tkinter
import tkinter as tk
from multiprocessing.connection import Listener

from pynput import mouse
import time
import threading


class Stopwatch:
    """
    A simple Stopwatch class to keep track of time
    """
    def __init__(self):
        self.start_time = time.time()
        self.delta = 0
        self.running = False
        self.thread = None

    def start(self):
        # Start only if not already running
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.delta  # Resume from current time
            self.thread = threading.Thread(target=self.start_timer, daemon=True)
            self.thread.start()

    def start_timer(self):
        # Update the timer while running
        while self.running:
            self.delta = time.time() - self.start_time
            time.sleep(0.01)  # Update every 10ms

    def stop(self):
        if self.running:
            self.running = False

    def reset(self):
        self.stop()
        self.delta = 0

    def __str__(self):
        if self.delta <= 0:
            return "00:00.000"
        minutes = int(self.delta // 60)
        seconds = int(self.delta % 60)
        milliseconds = int((self.delta % 1) * 1000)
        return f"{minutes:02}:{seconds:02}.{milliseconds:03}"




def update_timers():
    """
    Recursive function to update stopwatches
    """
    top_left_timer.config(text=str(timer1))     # Set the text of the label to the time
    bottom_left.config(text=str(timer2))    # Set the text of the label to the time
    window.after(50, update_timers)         # Update every 50 ms


def mouse_click_listener(x, y, button, pressed):
    """
    Mouse click listener
    """

    # Check if the button is pressed
    if pressed:

        # Check if the button is side button
        if button.name == "x2":

            timer1.reset()
            timer1.start()

        # Check if the button pressed is right click
        if button.name == "right":

            # Reset and start the timer
            timer2.reset()
            timer2.start()


def coloring_timers():
    """
    Apply different colors to the timers (timer1 and timer2) based on specific thresholds:
    - Timer1:
        0 -> 60 seconds: white
        60 -> 90 seconds: orange
        90 -> 180 seconds: red
        180+ seconds: gray
    - Timer2:
        <= 4 seconds: orange
        <= 5 seconds: red
        > 5 seconds: white
    """
    # Thresholds for timer1
    DEMON_SMUDGE = 60
    GENERIC_SMUDGE = 90
    SPIRIT_SMUDGE = 180

    # Thresholds for timer2
    SMUDGE_BLIND_PRE_WARNING = 4
    SMUDGE_BLIND_WARNING = 5

    # Infinite loop
    while True:

        # Timer1 logic
        if timer1.delta < DEMON_SMUDGE:
            top_left_timer.config(fg='white')       # 0 -> 60 seconds

        elif DEMON_SMUDGE <= timer1.delta < GENERIC_SMUDGE:
            top_left_timer.config(fg='orange')      # 60 -> 90 seconds

        elif GENERIC_SMUDGE <= timer1.delta < SPIRIT_SMUDGE:
            top_left_timer.config(fg='red')         # 90 -> 180 seconds

        else:
            top_left_timer.config(fg='gray')        # 180+ seconds

        # Timer2 logic
        if timer2.delta <= SMUDGE_BLIND_PRE_WARNING:
            bottom_left.config(fg='white')     # <= 4 seconds

        elif timer2.delta <= SMUDGE_BLIND_WARNING:
            bottom_left.config(fg='orange')        # <= 5 seconds

        else:
            bottom_left.config(fg='red')      # > 5 seconds

        time.sleep(0.1)



"""
def visualize_steps():
    DELAY = 0.5217

    while True:

        if visual_steps:

            visual_mark = tk.SOLID(window).grid(row=0, column=3)
"""



if __name__ == '__main__':

    # Le good spam
    print("ver 1")
    print("♥ Created by Carpetano ♥")
    print("► My Github: https://github.com/Carpetano/Overlay-Stopwatch\n")
    print("▫ Forward Mouse Button   → Timer 1 (Bottom-Left)")
    print("▫ Right Click            → Timer 2 (Top-Right)")

    # Initialize tkinter window
    window = tk.Tk()
    window.config(background='black')                   # Set bg as black
    window.attributes("-topmost", True)                 # Always on top
    window.attributes("-transparentcolor", "black")     # Make black color transparent
    window.overrideredirect(True)                       # Remove window decorations



    # Stopwatch instances
    timer1 = Stopwatch()
    timer2 = Stopwatch()


    # Top timer
    top_left_timer = tkinter.Label(window, text="00:00.000", font=('Helvetica', 28, 'bold'), fg='white', bg='black')
    top_left_timer.grid(row=1, column=1, padx=10, pady=10)

    # Bottom timer
    bottom_left = tkinter.Label(window, text="00:00.000", font=('Helvetica', 28, 'bold'), fg='gray', bg='black')
    bottom_left.grid(row=2, column=1, padx=10, pady=50)


    # Thread in charge of coloring
    threading.Thread(target=coloring_timers, daemon=True).start()

    # Thread in charge of listening for mouse input
    mouse.Listener(on_click=mouse_click_listener).start()


    # Start updating timers
    update_timers()

    # Start the tkinter main loop
    window.mainloop()
