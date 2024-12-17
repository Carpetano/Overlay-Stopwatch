import tkinter as tk
from pynput import mouse
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

def toggle_stopwatch():
    """Toggle the stopwatch between start, pause, and reset."""
    global is_stopwatch_running, start_time, elapsed_time

    # Start or reset the stopwatch
    reset_start_timer()

def reset_start_timer():
    """Reset the stopwatch and immediately start it in white color."""
    global is_stopwatch_running, elapsed_time, start_time

    elapsed_time = 0  # Reset elapsed time
    is_stopwatch_running = True  # Start the stopwatch
    start_time = time.time()  # Set start_time to the current time

    # Set the label color to white and reset text
    label.config(fg="white", text="00:00")

def update_display():
    """Update the stopwatch display."""
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

# Mouse listener for global right-clicks
def on_click(x, y, button, pressed):
    """Mouse listener for global clicks."""
    if button == mouse.Button.right and pressed:  # Check for right-click press
        toggle_stopwatch()

print("♥ Created by Carpetano ♥")
print("► My Github: https://github.com/Carpetano/Overlay-Stopwatch")
print("\n▫ Right-click to start / reset timer")
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

    # Start the mouse listener
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    # Start updating the display
    update_display()

    # Run the Tkinter loop
    root.mainloop()
