import tkinter as tk
from pynput import keyboard, mouse
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
    stopwatch1.config(text=str(timer1))
    stopwatch2.config(text=str(timer2))
    window.after(50, update_timers)  # Update every 50 ms


def on_click(x, y, button, pressed):
    """
    Mouse click listener
    """
    if pressed:  
        if button.name == "right":  
            timer2.reset()
            timer2.start()

def on_press(key):
    """
    Keyboard press listener
    """
    if key == keyboard.Key.alt_l:
        
        if timer1.running: timer1.stop()
        else: timer1.reset(); timer1.start()

def limit_timer(timer, max_time):
    while True:
        if timer.delta > max_time:
            timer.stop()
            timer.reset()
        else:
            time.sleep(0.1)

if __name__ == '__main__':

    print("♥ Created by Carpetano ♥")
    print("► My Github: https://github.com/Carpetano/Overlay-Stopwatch")
    print("\n▫ Alt / Right click to start timers")

    # Initialize tkinter window
    window = tk.Tk()
    window.config(background='black')
    window.attributes("-topmost", True)               # Always on top
    window.attributes("-transparentcolor", "black")   # Transparent
    window.overrideredirect(True)                     # Remove window decorations

    # Stopwatch instances
    timer1 = Stopwatch()
    timer2 = Stopwatch()

    # Labels for stopwatch display
    stopwatch1 = tk.Label(window, text="00:00", font=('Helvetica', 30, 'bold'), fg='white', bg='black')
    stopwatch1.grid(row=0, column=1, padx=10, pady=5)

    stopwatch2 = tk.Label(window, text="00:00.00", font=('Helvetica', 20, 'bold'), fg='white', bg='black')
    stopwatch2.grid(row=0, column=2)

    # Start updating timers
    update_timers()

    # Start the mouse listener in a separate thread
    mouse_thread = threading.Thread(target=lambda: mouse.Listener(on_click=on_click).start(), daemon=True).start()

    keyboard_thread = threading.Thread(target=lambda: keyboard.Listener(on_press=on_press).start(), daemon=True).start()

    TIME_LIMIT = 60

    mouse_thread_limiter = threading.Thread(target=limit_timer, args=(timer2, TIME_LIMIT)).start()

    # Start the tkinter main loop
    window.mainloop()
