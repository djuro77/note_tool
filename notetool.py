import pynput
from pynput.keyboard import Key, Listener
import pyperclip
import tkinter as tk
from threading import Thread

###   KEY LISTENER   ###

alt_count = 0
note_parts = []

def on_release(key):
    global note_parts
    #print(key)
    global alt_count
    if key == Key.alt_r:
        alt_count += 1

        if alt_count == 3:
            new_part = pyperclip.paste()
            T.insert(tk.END, f"{new_part}\n\n")
            # reset alt_count right away
            alt_count = 0
    else:
        alt_count = 0


def key_listener():
    with Listener(on_release=on_release) as listener:
        listener.join()

thread_listener = Thread(target=key_listener)
thread_listener.start()

###   FRONTEND   ###

def note_to_clipboard():
    pyperclip.copy(T.get("1.0", tk.END))

def command_always_on_top():
    if var_always_on_top.get() == 1:
        root.wm_attributes("-topmost", 1)
    else:
        root.wm_attributes("-topmost", 0)

root = tk.Tk()

mainframe = tk.Frame(root)
mainframe.grid(row=0)
text_frame = tk.Frame(root)
text_frame.grid(row=1)



S = tk.Scrollbar(text_frame)
T = tk.Text(text_frame)
B = tk.Button(mainframe, text="Copy", command=note_to_clipboard)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
var_always_on_top = tk.IntVar()
ckbox_always_on_top = tk.Checkbutton(mainframe, text="Always on top", variable=var_always_on_top, command=command_always_on_top)
B.grid(row=0, column=0)
ckbox_always_on_top.grid(row=0, column=1)
S.pack(side=tk.RIGHT, fill=tk.Y)
T.pack(side=tk.LEFT, fill=tk.Y)

root.mainloop()
