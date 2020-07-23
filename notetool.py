import pynput
from pynput.keyboard import Key, Listener
import pyperclip
import tkinter as tk
from threading import Thread

###   KEY LISTENER   ###
alt_count = 0

def on_release(key):
    global alt_count
    if key == Key.alt_r:
        alt_count += 1

        if alt_count == 3:
            new_part = pyperclip.paste()
            text.insert(tk.END, f"{new_part}\n\n")
            # reset alt_count right away
            alt_count = 0
    else:
        alt_count = 0


def key_listener():
    with Listener(on_release=on_release) as listener:
        listener.join()

thread_listener = Thread(target=key_listener)
thread_listener.start()


## Note Class
class Note:
    """Main class for Note objects -- intended to store generalised data"""

    def __init__(self, title=None, content=None):
        self.title = title
        self.content = content

    def get_frontendData(self):
        """returns JSON formated data"""
        return {
        "title": self.title,
        "content": self.content
        }


###   FRONTEND   ###
current_note = Note(title="TEST", content="Proba 1 2 3")
next_note = 0

## Button Command Functions
def note_to_clipboard():
    pyperclip.copy(text.get("1.0", tk.END))


def command_always_on_top():
    if var_always_on_top.get() == 1:
        root.wm_attributes("-topmost", 1)
    else:
        root.wm_attributes("-topmost", 0)


def command_clear():
    text.delete("1.0", tk.END)


def command_delete():
    pass


def _new_button_return(note):
    """returns function for command action for each new note button. """

    def return_function():
        global current_note

        # save the old current
        print(f"Current Note: {current_note.title}")
        print(f"--saving {current_note.title} ...")
        current_note.content = text.get("1.0", tk.END)
        print(f"{current_note.title} saved successfully +")

        # set new current as current
        print(f"--setting current to {note.title} ...")
        current_note = note
        print(f"Current Note: {current_note.title}\n")

        # label current update
        label_current_var.set(f"Curent: {note.title} ")

        # insert content of new current
        text.delete("1.0", tk.END)
        text.insert(tk.END, note.content)

    return return_function()


def command_newNote():

    """Actions when 'New' button is clicked"""

    global next_note
    next_note += 1

    # create new note object
    note = Note(title=str(next_note), content="")
    # create new button and display it in notes_frame
    button = tk.Button(notes_frame, text=note.title, width=6, command=lambda n=note: _new_button_return(n))
    button.grid(row=0, column=next_note, sticky="wn", padx=1)

    # call command_showNote() and load new as selected
    _new_button_return(note)


## Start MainLoop

## widget options
widOpt_MainFrameButtons = {"width":10, }
girdOpt_MainFrameButtons = {"sticky":"new", "padx":2}

root = tk.Tk()
root.grid_columnconfigure(0,weight=1) # the text and entry frames column
root.grid_rowconfigure(2,weight=1) # all frames row

mainframe = tk.Frame(root)
mainframe.grid(row=0, column=0, sticky="new")
#mainframe.grid_columnconfigure(1,weight=1) # the text and entry frames column
#mainframe.grid_rowconfigure(0,weight=1) # all frames row
notes_frame = tk.Frame(root)
notes_frame.grid(row=1, column=0, sticky="nw")
#notes_frame.grid_columnconfigure(1,weight=1) # the text and entry frames column
#notes_frame.grid_rowconfigure(0,weight=1) # all frames row
text_frame = tk.Frame(root)
text_frame.grid(row=2, column=0, sticky="nswe")
text_frame.grid_columnconfigure(0,weight=1) # the entry and text widgets column
text_frame.grid_rowconfigure(0,weight=1) # the text widgets row


# mainframe Widgets
label_current_var = tk.StringVar()
label_current = tk.Label(mainframe, bg="grey", textvariable=label_current_var, width=10)
label_current.grid(row=0, column=0, sticky=tk.W, padx=20)
button_copy = tk.Button(mainframe, **widOpt_MainFrameButtons, text="Copy", command=note_to_clipboard)
button_copy.grid(row=0, column=1, **girdOpt_MainFrameButtons)
button_clear = tk.Button(mainframe, **widOpt_MainFrameButtons, text="New", command=command_newNote)
button_clear.grid(row=0, column=2, **girdOpt_MainFrameButtons)
button_clear = tk.Button(mainframe, bg="red", **widOpt_MainFrameButtons, text="Clear", command=command_clear)
button_clear.grid(row=0, column=3, **girdOpt_MainFrameButtons)
button_delete = tk.Button(mainframe, state="disabled", **widOpt_MainFrameButtons, text="Delete", command=command_delete)
button_delete.grid(row=0, column=4, **girdOpt_MainFrameButtons)
var_always_on_top = tk.IntVar()
ckbox_always_on_top = tk.Checkbutton(mainframe, text="Always on top", variable=var_always_on_top, command=command_always_on_top)
ckbox_always_on_top.grid(row=0, column=5, sticky='e')

# text_frame Widgets
yscrollbar = tk.Scrollbar(text_frame)
yscrollbar.grid(row=0, column=1, sticky="nse")
text = tk.Text(text_frame, bd=0, yscrollcommand=yscrollbar.set)
text.grid(row=0, column=0, sticky="nswe")
yscrollbar.config(command=text.yview)

root.mainloop()
