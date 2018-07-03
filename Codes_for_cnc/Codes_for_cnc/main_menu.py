from tkinter import *
import os

global root2
global t_no_ent


def func_to_seed():
	fr.destroy()
	root.destroy()                   															
	
	os.system("python3 seed_window.py")

def func_to_water():
	fr.destroy()
	root.destroy()                   															
	
	os.system("python3 water_window.py")
def func_to_monitor():
	fr.destroy()
	root.destroy()                   															
	
	os.system("python3 monitor_window.py")

root = Tk()
tno=StringVar()
root.title("Welcome to GrowBox!")
root.geometry("1200x640")
fr=Frame(root)
fr.grid(row=0,column=0,columnspan=3,rowspan=3)
#****** Title *******
title=Label(fr,text="GrowBox Manager",fg="Green",font=("Courier",44,"bold"))
fr.grid_columnconfigure(1, weight=1)
fr.grid_rowconfigure(0, weight=1)
title.grid(row=0,column=1,padx=30)

#****** Image *******
photo=PhotoImage(file="greenbox1.png")
photo_label=Label(fr,image=photo,relief="groove",borderwidth=10)
fr.grid_columnconfigure(1, weight=1)
fr.grid_rowconfigure(1, weight=1)
photo_label.grid(column=1,row=1,pady=50)

#****** Options *******
fr.grid_columnconfigure(0, weight=1)
fr.grid_columnconfigure(1, weight=1)
fr.grid_columnconfigure(2, weight=1)
fr.grid_rowconfigure(3, weight=1)
seed=Button(fr,anchor=CENTER,text="SEED",command=func_to_seed,relief="sunken",borderwidth=3,width=20,height=2,font=("Courier",15),fg="blue",activebackground="black",activeforeground="white")
seed.grid(column=0,row=2,padx=30)
water=Button(fr,anchor=CENTER,text="WATER",command=func_to_water,relief="sunken",borderwidth=3,width=20,height=2,font=("Courier",15),fg="blue",activebackground="black",activeforeground="white")
water.grid(column=1,row=2)
monitor=Button(fr,anchor=CENTER,text="MONITOR",command=func_to_monitor,relief="sunken",borderwidth=3,width=20,height=2,font=("Courier",15),fg="blue",activebackground="black",activeforeground="white")
monitor.grid(column=2,row=2)


root.mainloop()
