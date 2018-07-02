from tkinter import *
import os
import datetime
from tkinter import messagebox
from functools import partial

global sub_but
global ip_trough_no
global tno1
global plant
global no_plants


def main_call():
	fr_s.destroy()
	root.destroy()                   															
	
	os.system("python3 main_menu.py")
def quit_call():
	fr_s.destroy()
	root.destroy()
def insert_details(tno1,plant,no_plants):
	#now = datetime.datetime.now()
	
	
    
	fout=open("seed_status.txt","w")
	currentDay = datetime.datetime.now().day
	currentMonth = datetime.datetime.now().month
	currentYear = datetime.datetime.now().year

	line_w=list()
	line_w.append("troughno: "+tno1.get()+"\n")
	line_w.append("status: seeded"+"\n")
	line_w.append("date of sowing: "+(str(currentDay)+"/"+str(currentMonth)+"/"+str(currentYear))+"\n")
	line_w.append("plant: "+plant.get()+"\n")
	line_w.append("no of plants: "+no_plants.get()+"\n")
	line_w.append("average growth: "+"0"+"\n")

	for line in line_w :
		fout.write(line)
	fout.close()
	os.system("python3 corner_grid_cal_7.py")
	os.system("python3 go_for_seed_1.py")
	
def print_details(ip_trough_no):
	fhand=open("seed_status.txt","r")
	
	i=-1
	st=str(ip_trough_no)
	st0="troughno: "
	info=list()
	for line in fhand :
		if line.startswith(st0+st) :
			i = 0
		if i!=(-1):
			info.append(Label(fr_s,text=line.upper(),fg="brown",font=("Courier",14,"bold"),anchor=W))
			fr_s.grid_columnconfigure(1, weight=1)
			fr_s.grid_rowconfigure(2+i, weight=1)
			info[i].grid(row=2+i,column=1,padx=10,pady=15)
			i+=1
		elif i==5 :
			break
	fhand.close()
	if i==-1 :
		
		checker=IntVar()
		plant=StringVar()
		no_plants=StringVar()
		tno1=StringVar()
		title1=Label(fr_s,text="Trough no.",fg="brown",font=("Courier",14,"bold"),anchor=W)
		fr_s.grid_columnconfigure(1, weight=1)
		fr_s.grid_rowconfigure(2, weight=1)
		title1.grid(row=2,column=1,padx=30,pady=20)
		fr_s.grid_columnconfigure(2, weight=1)
		t_no_ent1=Entry(fr_s,textvariable=tno1)
		t_no_ent1.grid(row=2,column=2,sticky=N+S+W+E,padx=30,pady=20)

		title2=Label(fr_s,text="Plant",fg="brown",font=("Courier",14,"bold"),anchor=W)
		fr_s.grid_columnconfigure(1, weight=1)
		fr_s.grid_rowconfigure(3, weight=1)
		title2.grid(row=3,column=1,padx=30,pady=20)
		fr_s.grid_columnconfigure(2, weight=1)
		plant_name=Entry(fr_s,textvariable=plant)
		plant_name.grid(row=3,column=2,sticky=N+S+W+E,padx=30,pady=20)

		title3=Label(fr_s,text="No. of plants",fg="brown",font=("Courier",14,"bold"),anchor=W)
		fr_s.grid_columnconfigure(1, weight=1)
		fr_s.grid_rowconfigure(4, weight=1)
		title3.grid(row=4,column=1,padx=30,pady=20)
		fr_s.grid_columnconfigure(2, weight=1)
		no_of_plants=Entry(fr_s,textvariable=no_plants)
		no_of_plants.grid(row=4,column=2,sticky=N+S+W+E,padx=30,pady=20)

		action_with_arg = partial(insert_details, tno1,plant,no_plants)
		sub_but.grid_remove()
		sub_but_2=Button(fr_s,text="Submit",command=action_with_arg,height=2,width=15)
		fr_s.grid_rowconfigure(4, weight=1)
		sub_but_2.grid(row=5,column=2)
		
 
		


def t_no_check(*args):
	try:
		if tno.get()!="1":
			messagebox.showinfo("Alert","Only 1 trough available !")
			tno.set("")
		else :
			ip_trough_no=int(tno.get())

			print_details(ip_trough_no)
	except ValueError:
		print("error")



root=Tk()
root.title("GrowBox: SEED")
root.geometry("1200x640")
	
fr_s=Frame(root)
fr_s.grid(row=0,column=0,columnspan=8,rowspan=8,sticky=N+S+E+W)

title=Label(fr_s,text="GrowBox Manager",fg="Green",font=("Courier",44,"bold"),anchor=CENTER)
fr_s.grid_columnconfigure(1, weight=1)
fr_s.grid_rowconfigure(0, weight=1)
title.grid(row=0,column=1,padx=30,pady=20,columnspan=3)

fr_s.grid_columnconfigure(0, weight=1)
fr_s.grid_rowconfigure(1, weight=1)
truf_label=Label(fr_s,text="Trough No.:",fg="brown",font=("Courier",24,"bold"))
truf_label.grid(row=1,column=0,padx=10)

fr_s.grid_columnconfigure(1,weight=1)
tno=StringVar()	
t_no_ent=Entry(fr_s,textvariable=tno)
t_no_ent.grid(row=1,column=1,sticky=N+S+W+E)

fr_s.grid_columnconfigure(2,weight=1)
sub_but=Button(fr_s,text="Submit",command=t_no_check,height=2,width=15)
sub_but.grid(row=1,column=2)

fr_s.grid_rowconfigure(7,weight=1)
fr_s.grid_columnconfigure(2,weight=1)
quit=Button(fr_s,text="QUIT",command=quit_call,height=2,width=15)
quit.grid(row=7,column=2,padx=20,pady=20)
fr_s.grid_columnconfigure(3,weight=1)
main_menu=Button(fr_s,text="Main Menu",command=main_call,height=2,width=15)
main_menu.grid(row=7,column=3,padx=20,pady=20)

t_no_ent.focus()
root.mainloop()
