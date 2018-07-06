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
#from coordinate_initialization import *

#************Variables******************
global mm_per_pix
global corner_finder
global curr_x
global curr_y
global curr_z
global hard_coord_x
global hard_coord_y
global pix_per_mm
global no_of_iterations
global trough_points
global grid_p
global hsquares
global frame_no
global frame
global ret
global reso
global ini_x
global ini_y
global ini_z
#************Initialization*************
frame_no=0
curr_x=0
curr_y=0
curr_z=0
ser = serial.Serial('/dev/ttyACM1',9600)
#hsquares=6
arduino_confirm = False
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)
comm_string=""
corner_finder=0
mm_per_pix=0.38557213
pix_per_mm=2.739751871
no_of_iterations = 0
hard_coord_x=0
hard_coord_y=0
fhand=open("trough_corner.txt","w")
trough_points=list()
grid_p=list()

#**************************************

#************Functions******************
#**********************************************************
#  * Function Name:get_data
#  * Input: none
#  * Output: none
#  * Logic: opens file seed_status.txt and initializes hsquares
#  * Example Call: get_data()
#**********************************************************
def get_data():
    global hsquares
    fhand_h=open("seed_status.txt","r")
    
    for line in fhand_h :
        if line.startswith("no of plants"):
            index=line.find(":")
            hsquares=int(line[index+2])/2
            
    fhand_h.close()
    print(hsquares)

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
	comm_string="@"+str(ini_x+50).zfill(4)+str(ini_y+20).zfill(3)+str(ini_z).zfill(3)+"000"+"!"
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
#Function Name:go_at_start
#  * Input: none
#  * Output: none
#  * Logic: will go to suitable place to start corner finding 
#			from.
#  * Example Call: go_at_start()
#**********************************************************
#def go_at_start():
#	pass
def get_coordinate():
	global curr_x
	global curr_y
	global curr_z
	global frame_no
	global frame
	global ret
	global reso
	#cap = cv2.VideoCapture(0)
	#cap.set(3,1280)
	#cap.set(4,1024)
	cap.set(15,1.1)
	#print(reso)
	#time.sleep(4)
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
		print(curr_x)
		print(curr_y)
		img = cv2.drawContours(frame,[box],0,(255,0,0),2)
		cv2.imwrite("img%s.jpg"%str(frame_no).zfill(2),frame)
		frame_no=frame_no+1

#**********************************************************
#Function Name:hard_distance
#  * Input: int-to choose how much distance
#               to move before image_process
#				starts to find corner
#  * Output: none
#  * Logic: will generate the serial string
# 			and communicate to arduino, followed
#			by confirmation 
#  * Example Call: hard_distance(0)
#**********************************************************
def hard_distance(number):
	global curr_x
	global curr_z
	global curr_y
	global mm_per_pix
	global hard_coord_x
	global hard_coord_y
	global no_of_iterations
	global arduino_confirm
	if number == 0 :
			hard_coord_x = curr_x+30*no_of_iterations*0
	elif number == 1 :
			hard_coord_x = 750 
	elif number == 2 :
			hard_coord_y=450

	arduino_confirm=False
	mystring=""
	if corner_finder < 2 :
		if no_of_iterations == 0:
			comm_string="@"+str(hard_coord_x).zfill(4)+str(curr_y).zfill(3)+str(curr_z).zfill(3)+"001"+"!"
		else :
			comm_string="@"+str(hard_coord_x).zfill(4)+str(curr_y).zfill(3)+str(curr_z).zfill(3)+"000"+"!"
	else : 
			comm_string="@"+str(curr_x).zfill(4)+str(hard_coord_y).zfill(3)+str(curr_z).zfill(3)+"000"+"!"
	ser.write(comm_string.encode("ascii"))
	print(comm_string)
	while arduino_confirm == False :
		line_in=ser.readline()
		for char in line_in:
			mystring = mystring + chr(char)
		if mystring == "@done!\n":
			if corner_finder < 2 :
				curr_x = hard_coord_x
			else :
				curr_y = hard_coord_y
			arduino_confirm=True	
		#arduino_confirm=True

#**********************************************************
#Function Name:image_process_for_corner
#  * Input: none
#  * Output: none
#  * Logic: run image processing code for corner detection
#			if found update file trough_corner.txt
#			if found update corner_finder
#			update no_of_iterations
#			
#  * Example Call: image_process_for_corner()
#**********************************************************
def image_process_for_corner():
	global curr_x
	global curr_y
	global curr_z
	global mm_per_pix
	global corner_finder
	global frame_no
	global trough_points
	global frame
	global ret
	global reso
	cap = cv2.VideoCapture(0)
	#time.sleep(24)
	cap.set(3,1280)
	cap.set(4,1024)
	#time.sleep(5)
	cap.set(15,1.0)
	#time.sleep(5)
	ret, frame = cap.read()
	#print("hi")
	#time.sleep(1)
	cap.release()
	#if corner_finder == 0:
            #frame=cv2.imread("img00.jpg")
	if ret :
		hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		print("in")
		lower_range=np.array([90,70,70])
		higher_range=np.array([120,255,255])
		mask1 = cv2.inRange(hsv,lower_range,higher_range)
		res = cv2.bitwise_and(frame,frame, mask=mask1)
		ret,thrshed = cv2.threshold(cv2.cvtColor(res,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
		image,contours,hier = cv2.findContours(thrshed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		cv2.imwrite("test.jpg",frame)
		print("done")
		#time.sleep(2)
		area = 0
		for cnt in contours :
			area = cv2.contourArea(cnt)
			if area>3000 :
				rect = cv2.minAreaRect(cnt)
				print(area)
				time.sleep(2)
				box = cv2.boxPoints(rect)
				box = np.int0(box)
				x4,y4=box[0]
				x3,y3=box[1]
				x1,y1=box[2]
				x2,y2=box[3]
				img = cv2.drawContours(frame,[box],-1,(0,0,255),2)
				#cv2.imwrite("img%s.jpg"%str(frame_no).zfill(2),frame)  #debug
				xc,yc=(640,512)
				xt,yt=get_ratio_points(x1,x2,y1,y2,1,1)
				xd,yd=get_ratio_points(x4,x3,y4,y3,1,1)
				xs,ys=get_ratio_points(xt,xd,yt,yd,1,1)
				cv2.circle(frame,(xs,ys),5,(0,0,255),-1)
				cv2.imwrite("img%s.jpg"%str(frame_no).zfill(2),frame)
				point_y=(xs-xc)*mm_per_pix
				point_x=(ys-yc)*mm_per_pix
				corner_x=curr_x-point_x
				corner_y=curr_y-point_y
				#print(point_x)
				#print(point_y)
				print(corner_x)
				print(corner_y)
				trough_points.append((corner_x,corner_y))
				file_string="point"+str(corner_finder)+ ":"+str(corner_x)+" "+str(corner_y)+"\n"
				fhand.write(file_string)	
				corner_finder=corner_finder+1
				frame_no=frame_no+1


#**********************************************************
#Function Name:get_fourth_point
#  * Input: 3 corners of the trough
#  * Output: 4th corner of the trough
#  * Logic: linear coordinate geometry formulas
#  * Example Call: get_fourth_point(1,2,3,4,5,6)
#**********************************************************
def get_fourth_point(x1,x2,x4,y1,y2,y4):
	m1=(y2-y4)/(x2-x4)
	m2=(y1-y2)/(x1-x2)
	x3=(y1-y4-(m1*x1)+(m2*x4))/(m2-m1)
	y3=m2*(x3-x4)+y4
	print(m1*m2)
	return (int(x3),int(y3))

#**********************************************************
#Function Name:get_grids
#  * Input: two points of the line on which grid points 
#			will lie
#  * Output: none 
#  * Logic: linear coordinate geometry formulas
#  * Example Call: get_grids()
#**********************************************************
def get_grids(x1,x2,y1,y2):
	global hsquares
	global grid_p
	k1=1
	k2=hsquares
	i=0
	while k1 <= (hsquares):
		grid_p.append(get_ratio_points(x1,x2,y1,y2,k1,k2))
		k1=k1+1
		k2=k2-1
		i=i+1

#**********************************************************
#Function Name:get_grid_points
#  * Input: 4 corners of the trough
#  * Output: none
#  * Logic: linear coordinate geometry formulas
#  * Example Call:get_grid_points(1,2,3,4,5,6,7,8)
#**********************************************************
def get_grid_points(x1,x2,x3,x4,y1,y2,y3,y4):
  xa,ya = get_ratio_points(x1,x2,y1,y2,1.5,3.5)
  xb,yb = get_ratio_points(x1,x2,y1,y2,3.5,1.5)
  xc,yc = get_ratio_points(x3,x4,y3,y4,1.5,3.5)
  xd,yd = get_ratio_points(x3,x4,y3,y4,3.5,1.5)
  get_grids(int(xa),int(xc),int(ya),int(yc))
  get_grids(int(xb),int(xd),int(yb),int(yd))
#**********************************************************
#Function Name:create_grid
#  * Input: none
#  * Output: none
#  * Logic: to calculate the 4th point of trough and consequently
#			all grid points and store the same in file 
#			grid_points.txt
#  * Example Call: create_grid()
#**********************************************************
def create_grid():
	x4,y4=trough_points[0] #cnc coordinate
	x2,y2=trough_points[1]
	x1,y1=trough_points[2]
	#x4,y4=(124,172)
	#x2,y2=(780,78)
	#x1,y1=(797,419)
    
	x3,y3=get_fourth_point(x1,x2,x4,y1,y2,y4)
	print("fourth")
	print(x3,y3)
	get_grid_points(x1,x2,x3,x4,y1,y2,y3,y4)
	fin = open("grid_points.txt","w")
	temp=""
	plant_no_for_file=1
	for points in grid_p :
		temp="plant"+str(plant_no_for_file)+":"+str(points[0])+" "+str(points[1])+"\n"
		plant_no_for_file=plant_no_for_file+1
		fin.write(temp)
	fin.close()


#**********************************************************
#Function Name:find_corners
#  * Input: none
#  * Output: none
#  * Logic: click pictures and process it continually for 
#			detecting corners 
#  * Example Call: find_corners()
#**********************************************************
def find_corners():
	global no_of_iterations
	global corner_finder
	#time.sleep(5)
	get_coordinate()
	get_ini_coord()
	get_data()
	corner_finder=0
	no_of_iterations=0
	while corner_finder < 3 :
		hard_distance(corner_finder)
		image_process_for_corner()
		no_of_iterations=no_of_iterations+1
	fhand.close()
	go_to_start()
	create_grid()
		
		
find_corners()

#create_grid()
#cap.release()


