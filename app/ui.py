from tkinter import Tk
from tkinter.ttk import Button, Frame, Label

def run():
    root = Tk()
    root.title("Example application")

    frame = Frame(root, padding=20)
    frame.pack()

    label = Label(frame, text="Hello, World!")
    label.pack()

    button = Button(frame, text="Click Me", command=lambda: label.config(text="Button clicked"))
    button.pack(pady=20)

    root.mainloop()

