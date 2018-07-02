from tkinter import *
import os
import datetime
from tkinter import messagebox
from functools import partial


def main_call():
	fr_m.destroy()
	root.destroy()                   															
	
	os.system("python3 main_menu.py")
def quit_call():
	fr_m.destroy()
	root.destroy()
def t_no_check(*args):
	try:
		if tno.get()!="1":
			messagebox.showinfo("Alert","Only 1 trough available !")
			tno.set("")
	except ValueError:
		print("error")

root=Tk()
root.title("GrowBox: Monitor")
root.geometry("1200x640")

fr_m=Frame(root)
fr_m.grid(row=0,column=0,columnspan=8,rowspan=8,sticky=N+S+E+W)

title=Label(fr_m,text="GrowBox Manager",fg="Green",font=("Courier",44,"bold"),anchor=CENTER)
fr_m.grid_columnconfigure(1, weight=1)
fr_m.grid_rowconfigure(0, weight=1)
title.grid(row=0,column=1,padx=30,pady=20,columnspan=3)

fr_m.grid_columnconfigure(0, weight=1)
fr_m.grid_rowconfigure(1, weight=1)
truf_label=Label(fr_m,text="Trough No.:",fg="brown",font=("Courier",24,"bold"))
truf_label.grid(row=1,column=0,padx=10)

fr_m.grid_columnconfigure(1,weight=1)
tno=StringVar()	
t_no_ent=Entry(fr_m,textvariable=tno)
t_no_ent.grid(row=1,column=1,sticky=N+S+W+E)

fr_m.grid_columnconfigure(2,weight=1)
sub_but=Button(fr_m,text="Submit",command=t_no_check,height=2,width=15)
sub_but.grid(row=1,column=2)

fr_m.grid_rowconfigure(7,weight=1)
fr_m.grid_columnconfigure(2,weight=1)
quit=Button(fr_m,text="QUIT",command=quit_call,height=2,width=15)
quit.grid(row=7,column=2,padx=20,pady=20)
fr_m.grid_columnconfigure(3,weight=1)
main_menu=Button(fr_m,text="Main Menu",command=main_call,height=2,width=15)
main_menu.grid(row=7,column=3,padx=20,pady=20)

t_no_ent.focus()
root.mainloop()
