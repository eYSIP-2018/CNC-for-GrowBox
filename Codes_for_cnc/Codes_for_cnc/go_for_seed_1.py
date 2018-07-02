#**********************************************************
#  * Function Name:
#  * Input: 
#  * Output: 
#  * Logic: 
#  * Example Call: ()
#**********************************************************

import cv2
import numpy as np
import math
import serial
import os
import time

#************Variables******************

global hsquares
global g_points
global curr_x
global curr_y
global curr_z
global arduino_confirm
global mm_per_pix
global ini_x
global ini_y
global ini_z
#************Initialization*************

mm_per_pix=0.38557213
curr_z=0
curr_y=0
curr_x=0
arduino_confirm = False
g_points=list()
ser = serial.Serial('/dev/ttyACM1',9600)
comm_string=""
#**********************************************************
#Function Name:go_to_start
#  * Input: none
#  * Output: none
#  * Logic: will go to suitable place to start corner finding 
#			from.
#  * Example Call: go_to_start()
#**********************************************************
def go_to_start():
	global ini_x
	global ini_y
	global ini_z
	arduino_confirm=False
	mystring=""
	comm_string="@"+str(ini_x).zfill(4)+str(ini_y).zfill(3)+str(ini_z).zfill(3)+"000"+"!"
	ser.write(comm_string.encode("ascii"))
	print(comm_string)
	while arduino_confirm == False :
		line_in=ser.readline()
		for char in line_in:
			mystring = mystring + chr(char)
		if mystring == "@done!\n":
			arduino_confirm=True
#**********************************************************
#  * Function Name:get_ini_coord
#  * Input: none
#  * Output: none
#  * Logic: gets the initial coordinate of the CNC to return 
#           after every each seeding attempt and consequently
# 			at end also.
#  * Example Call: get_ini_coord()
#**********************************************************
def get_ini_coord():
	global ini_x
	global ini_y
	global ini_z
	global curr_x
	global curr_y
	global curr_z
	ini_x=curr_x
	ini_y=curr_y
	ini_z=curr_z
	arduino_confirm=False
	mystring=""
	comm_string="@"+str(ini_x).zfill(4)+str(ini_y).zfill(3)+str(ini_z).zfill(3)+"001"+"!"
	ser.write(comm_string.encode("ascii"))
	print(comm_string)
	while arduino_confirm == False :
			line_in=ser.readline()
			for char in line_in :
				mystring = mystring + chr(char)
			if mystring == "@done!\n":
				arduino_confirm=True
				
#**********************************************************
#  * Function Name:get_ratio_points
#  * Input: 2 points forming a line to be divided
#			ratios k1 and k2 in which line has to be divided 
#  * Output: point dividing the line in ratios k1 and k2
#  * Logic: linear coordinate geometry formulas
#  * Example Call:get_ratio_points(1,1,2,2,1,1)
#**********************************************************
def get_ratio_points(x1,x2,y1,y2,k1,k2):
  x0 = ((x1*k2)+(x2*k1))/(k1+k2)
  y0 = ((y1*k2)+(y2*k1))/(k1+k2)
  return int(x0),int(y0)
#**********************************************************
#  * Function Name:cal_distance_for_red
#  * Input: coordinates of red origin box
#  * Output: none
#  * Logic: simple linear geometry formulas
#  * Example Call: cal_distance_for_red(1,1,1,1,2,3,4,5)
#**********************************************************
def cal_distance_for_red(x1,x2,x3,x4,y1,y2,y3,y4):
	global curr_x
	global curr_y
	global curr_z
	global mm_per_pix
	xc,yc=(640,512)
	yr=512
	xt,yt=get_ratio_points(x1,x2,y1,y2,1,1)
	xd,yd=get_ratio_points(x4,x3,y4,y3,1,1)
	xs,ys=get_ratio_points(xt,xd,yt,yd,1,1)
	curr_y=int((xs-xc)*mm_per_pix)
	curr_x=int((ys-yc)*mm_per_pix)
	curr_z=0
#**********************************************************
#  * Function Name:get_coordinate
#  * Input: none
#  * Output: none
#  * Logic: will get the initial coordinates of the CNC mechanism
#  * Example Call: get_coordinate()
#**********************************************************
def get_coordinate():
	global curr_x
	global curr_y
	global curr_z
	cap = cv2.VideoCapture(0)
	cap.set(3,1280)
	cap.set(4,1024)
	cap.set(15,1.1)
	ret, frame = cap.read()
	cap.release()
	if ret :
		hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		lower_range=np.array([172,65,65])
		higher_range=np.array([180,255,255])
		mask1 = cv2.inRange(hsv,lower_range,higher_range)
		res = cv2.bitwise_and(frame,frame, mask=mask1)
		ret,thrshed = cv2.threshold(cv2.cvtColor(res,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
		image,contours,hier = cv2.findContours(thrshed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		areas = [cv2.contourArea(c) for c in contours]
		max_index = np.argmax(areas)
		cnt=contours[max_index]
		rect = cv2.minAreaRect(cnt)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		x4,y4=box[0]
		x3,y3=box[1]
		x1,y1=box[2]
		x2,y2=box[3]
		cal_distance_for_red(x1,x2,x3,x4,y1,y2,y3,y4)
		roi = cv2.resize(frame,(800,800))
		cv2.imwrite("test.jpg",roi)
		print(curr_x)
		print(curr_y)
#**********************************************************
#  * Function Name:get_data
#  * Input: none
#  * Output: none
#  * Logic: will extract all grid points from grid_points.txt
#  * Example Call: get_data()
#**********************************************************
def get_data():
	global g_points
	fhand_g=open("grid_points.txt","r")
	for line in fhand_g :
		index=line.find(':')
		index=index+1 
		x_coord=int(line[index:index+3])
		y_coord=int(line[index+4:index+7])
		g_points.append((x_coord,y_coord))
#**********************************************************
#  * Function Name:motor_for_seed
#  * Input: none
#  * Output: none
#  * Logic: will go for seeding in all the grid points as 
#			requested by the user through GUI 
#  * Example Call: motor_for_seed()
#**********************************************************
def motor_for_seed():
	global g_points
	global curr_x
	global curr_z
	global curr_y

	get_coordinate()
	get_ini_coord()
	get_data()
	iter=0

	for point in g_points :
		arduino_confirm=False
		mystring=""
		comm_string="@"+str(point[0]).zfill(4)+str(point[1]).zfill(3)+"000"+"000"+"!"
		ser.write(comm_string.encode("ascii"))
		print(comm_string)
		while arduino_confirm == False :
			line_in=ser.readline()
			for char in line_in:
				mystring = mystring + chr(char)
			if mystring == "@done!\n":
				arduino_confirm=True
				iter=iter+1
				go_to_start()
				get_coordinate()
				get_ini_coord()

motor_for_seed()
