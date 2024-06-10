from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from PIL import Image, ImageTk
import os

# Variables to track file path and changes
file_path = None
text_changed = False

# Creating all the functions of all the buttons in the Deregtext
def open_file():
    """
    Function to open files.
    The default extension is ".dgt"
    """

    global file_path, text_changed
    file = fd.askopenfilename(
        defaultextension=".dgt",
        filetypes=[("All Files", "*.*"), ("Text File", "*.dgt")],
    )

    if file != "":
        root.title(f"{os.path.basename(file)}")
        text_area.delete(1.0, END) # This deletes all text in the text area
        with open(file, "r") as file_:
            text_area.insert(1.0, file_.read())
            file_.close()
        file_path = file
        text_changed = False
    else:
        file = None


def open_new_file():
    """
    Opens a new file and deletes all content in the text area.
    """

    global file_path, text_changed
    root.title("Untitled - Deregtext")
    text_area.delete(1.0, END)
    file_path = None
    text_changed = False

def save_file():
    """
    Function to save file.
    Provides defaults for the user to overwrite.
    """

    global file_path, text_changed
    if file_path is None:
        file_path = fd.asksaveasfilename(
        initialfile="Untitled.dgt",
        defaultextension=".dgt",
        filetypes=[
            ("Text File", "*.txt"),
            ("Word Document", "*.docx"),
            ("PDF", "*.pdf"),
        ],
    )
        if not file_path:
            return

    with open(file_path, "w") as file:
        file.write(text_area.get(1.0, END))
    root.title(f"{os.path.basename(file_path)} - Deregtext")
    text_changed = False


def exit_application():
    if text_changed:
        response = mb.askyesnocancel("Save changes", "Do you want to save your changes?")
        if response: # Yes
            save_file()
            root.destroy()
        elif response is None:  # Cancel
            return
        else:   # No
            root.destroy()
    else:
        root.destroy()

def on_text_change(event=None):
    global text_changed
    text_changed = True
def copy_text():
    text_area.event_generate("<<Copy>>")


def cut_text():
    text_area.event_generate("<<Cut>>")


def paste_text():
    text_area.event_generate("<<Paste>>")


def select_all():
    """
    Function to select all text within the text area.
    'sel' defines the selection while '1.0' denotes the
    start point and the end point is 'end'
    """
    text_area.tag_add("sel", "1.0", "end")
    return "break"


def delete_last_char():
    text_area.event_generate("<<KP_Delete>>")


def about_deregtext():

    aboutdereg = """
    About Deregtext
    
    This is the first application from the DeregSoftware suite 
    of apps. In reality, this is a coding project to learn 
    Python. I have learned a bit as I've squashed bugs and 
    implemented some features. Stay tuned.
    """

    custom_dialog1 = Toplevel(root)
    custom_dialog1.title("About Deregtext")
    custom_dialog1.geometry("610x400")

    label = Label(custom_dialog1, text=aboutdereg, justify=LEFT)
    label.pack(padx=10, pady=10)

    button = Button(custom_dialog1, text="OK", command=custom_dialog1.destroy)
    button.pack(pady=10)


def about_commands():
    commands = """
    Under the File Menu:
    - 'New' clears the entire Text text_area
    - 'Open' clears text and opens another file
    - 'Save As' saves your file in the same / another extension

    Under the Edit Menu:
    - 'Copy' copies the selected text to your clipboard
    - 'Cut' cuts the selected text and removes it from the text area
    - 'Paste' pastes the copied/cut text
    - 'Select All' selects the entire text
    - 'Delete' deletes the last character
    """

    custom_dialog = Toplevel(root)
    custom_dialog.title("All commands")
    custom_dialog.geometry("610x500")

    label = Label(custom_dialog, text=commands, justify=LEFT)
    label.pack(padx=10, pady=10)

    button = Button(custom_dialog, text="OK", command=custom_dialog.destroy)
    button.pack(pady=10)


def main():
    """
    Main is defined to allow remote execution of program.
    This helps ensure that all necessary items are loaded
    before the program can be executed, else, the executer
    will error out.
    """

    global root, text_area

    # Initializing the window to create python text editor
    root = Tk()
    root.title("Untitled - Deregtext")
    root.geometry("1000x700")
    root.resizable(TRUE, TRUE)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    icon = ImageTk.PhotoImage(Image.open("media/img/Notepad.png"))
    root.iconphoto(False, icon)

    # Create the context menu
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="Copy", command=copy_text)
    context_menu.add_command(label="Cut", command=cut_text)
    context_menu.add_command(label="Paste", command=paste_text)
    context_menu.add_separator()
    context_menu.add_command(label="Select All", command=select_all)
    context_menu.add_command(label="Delete", command=delete_last_char)

    def show_context_menu(event):
        context_menu.post(event.x_root, event.y_root)

    def hide_context_menu(event):
        context_menu.unpost()

    # Create the menu bar
    menu_bar = Menu(root)

    # Adding the File Menu and its components to create Python Text Editor
    file_menu = Menu(menu_bar, tearoff=False, activebackground="DodgerBlue")

    file_menu.add_command(label="New", command=open_new_file)
    file_menu.add_command(label="Open File", command=open_file)
    file_menu.add_command(label="Save As", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Close File", command=exit_application)

    menu_bar.add_cascade(label="File", menu=file_menu)

    # Adding the Edit Menu and its components
    edit_menu = Menu(menu_bar, tearoff=False, activebackground="DodgerBlue")

    edit_menu.add_command(label="Copy", command=copy_text)
    edit_menu.add_command(label="Cut", command=cut_text)
    edit_menu.add_command(label="Paste", command=paste_text)
    edit_menu.add_separator()
    edit_menu.add_command(label="Select All", command=select_all)
    edit_menu.add_command(label="Delete", command=delete_last_char)

    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    # Adding the Help Menu and its components
    help_menu = Menu(menu_bar, tearoff=False, activebackground="DodgerBlue")

    help_menu.add_command(label="About Deregtext", command=about_deregtext)
    help_menu.add_command(label="About Commands", command=about_commands)

    menu_bar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menu_bar)

    # Setting the basic components of the window
    text_area = Text(root, font=("Times New Roman", 12))
    text_area.grid(sticky=NSEW)

    scroller = Scrollbar(text_area, orient=VERTICAL)
    scroller.pack(side=RIGHT, fill=Y)

    scroller.config(command=text_area.yview)
    text_area.config(yscrollcommand=scroller.set)

    # Bind the select_all function to a keyboard shortcut (Ctrl+A)
    root.bind("<Control-a>", select_all)

    # Bind the right-click event to show the context menu
    text_area.bind("<Button-3>", show_context_menu)

    # Bind the left-click event to hide the context menu
    text_area.bind("<Button-1>", hide_context_menu)

    # Bind text change event to track changes
    text_area.bind('<<Modified>>', on_text_change)

    # Give the text area focus when the application starts
    text_area.focus_set()

    # Overrie the window close button to prompt to save changes
    root.protocol("WM_DELETE_WINDOW", exit_application)
    # Finalizing the window
    # root.update()
    root.mainloop()


if __name__ == "__main__":
    main()
