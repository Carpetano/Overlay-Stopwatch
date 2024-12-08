import tkinter as tk
from pynput import keyboard
import time


# Global variables
is_stopwatch_running = False
elapsed_time = 0
start_time = None


def format_time(seconds):
    """Convert seconds to a MM:SS format."""
    minutes = int(seconds // 60)            # Get whole minutes
    seconds = int(seconds % 60)             # Get remaining seconds
    return f"{minutes:02}:{seconds:02}"     # Always show 2 digits for minutes and seconds


def toggle_stopwatch(key):
    """Toggle the stopwatch between start, pause, and reset."""

    # Set variables as global variables
    global is_stopwatch_running, start_time, elapsed_time 

    # Check if the pressed key is Left Alt
    if key == keyboard.Key.alt_l:  

        # If it's running, pause it, otherwise reset it
        pause_timer() if is_stopwatch_running else reset_start_timer()


def pause_timer():
    """Pause the timer and color it red."""

    # Set variables as global variables
    global is_stopwatch_running, elapsed_time

    # Stop the timer
    is_stopwatch_running = False  

    # Add time passed to elapsed_time
    elapsed_time += time.time() - start_time  

    # Change color to red
    label.config(fg="red")  


def reset_start_timer():
    """Reset the stopwatch and immediately start it in white color."""
    
    # Set variables as global variables
    global is_stopwatch_running, elapsed_time, start_time

    # Reset elapsed time
    elapsed_time = 0  

    # Start the stopwatch
    is_stopwatch_running = True  

    # Set start_time to the current time
    start_time = time.time()  

    # Set the label color to white and reset text
    label.config(fg="white", text="00:00")  


def update_display():
    """Update the stopwatch display."""

    # Set variables as global variables
    global elapsed_time, start_time

    if is_stopwatch_running:

        # Calculate the delta time
        delta = time.time() - start_time + elapsed_time

        # Update the display
        label.config(text=format_time(delta))

    else:
        # Show the elapsed time until the pause point
        label.config(text=format_time(elapsed_time))
    
    # Update the display every 100ms
    root.after(100, update_display)


# Keyboard listener for global key presses
def on_press(key):
    """Keyboard listener for global key presses"""
    try:
        toggle_stopwatch(key)
    except AttributeError:
        pass

print("♥ Created by Carpetano ♥")
print("► My Github: https://github.com/Carpetano/Overlay-Stopwatch")
print("\n▫ Press alt to start / reset timer")
print("▫ White = Running ; Red = Stopped")

if __name__ == '__main__':

    # Create overlay window
    root = tk.Tk()
    root.geometry("180x80")                         # Size and position
    root.attributes("-topmost", True)               # Always on top
    root.attributes("-transparentcolor", "black")   # Transparent
    root.attributes("-alpha", 0.8)                  # Make window semi-transparent
    root.overrideredirect(True)                     # Remove window decorations

    # Label to display the time
    label = tk.Label(root, text="00:00", font=("Helvetica", 38), fg="red", bg="black")
    label.pack(expand=True, fill="both")

    # Start the keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Start updating the display
    update_display()

    # Run the Tkinter loop
    root.mainloop()
