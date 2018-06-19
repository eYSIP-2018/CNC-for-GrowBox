from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass
    
root = Tk()
root.title("Feet to Meters")
mainframe = ttk.Frame(root, padding="60 60 240 240")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet, exportselection=0)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
#ttk.Checkbutton(mainframe, text="On", variable=checker, onvalue=1, offvalue=0).grid(column=1, row=1, sticky=(N,W,S,E))
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
#root.bind('<Button-1>', calculate)

root.mainloop()