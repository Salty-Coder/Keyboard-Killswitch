import sys
import os
import time
import threading


import tkinter as tk
from tkinter import scrolledtext
from tkinter import font


sys.path.append(os.path.abspath("keyboard"))
import keyboard


detonated = False

def detonate():
    global detonated
    detonated = True
    print("Detonation")
    file_path = 'test.txt'
    open_fullscreen_text_file(file_path)
    exit()



def open_fullscreen_text_file(file_path, window_width=800, window_height=600, font_size=70):
    root = tk.Tk()

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window position and size
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.title("Text Viewer")

    custom_font = font.Font(family="Base 05", size=font_size)

    text_widget = scrolledtext.ScrolledText(root, wrap='word', font=custom_font)
    text_widget.pack(expand=True, fill='both')

    with open(file_path, 'r') as file:
        text_widget.insert(tk.END, file.read())

    root.wm_attributes("-topmost", True)
    text_widget.configure(state='disabled')
    def on_closing():
        pass  # Do nothing

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Create a borderless window
    root.overrideredirect(True)
    # Prevent window from being moved around
    def reset_window_position():
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        if not fullscreen:
            root.after(700, reset_window_position)  # Reset position every 700ms
    reset_window_position()

    root.mainloop()


counting = False

def countdown():
    global counting
    counting = True
    for i in range(5, 0, -1):
        print(f"Countdown: {i} seconds left")
        for _ in range(5):  # Check every 0.2 seconds
            if keyboard.is_pressed('caps lock'):
                print("Space key pressed again, resetting countdown")
                counting = False
                return
            time.sleep(0.2)
    detonate()



def on_release(event):
    global counting
    global countdown_thread
    if event.name == 'caps lock' and event.event_type == keyboard.KEY_UP:
        if not detonated and not counting:
            countdown_thread = threading.Thread(target=countdown)
            countdown_thread.start()


keyboard.on_release(on_release)


countdown_thread = None

# End on ESC key
keyboard.wait('shift + esc')