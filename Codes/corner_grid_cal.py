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
from coordinate_initialization import *

#************Variables******************

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
#************Initialization*************

hsquares=6
arduino_confirm = False
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)
time.sleep(2)
comm_string=""
corner_finder=0
mm_per_pix=0.364996557
pix_per_mm=2.739751871
no_of_iterations = 0
hard_coord_x=0
hard_coord_y=0
fhand=open("trough_corner.txt","a")
trough_points=list()
grid_p=list()

#**************************************

#************Functions******************

#**********************************************************
#Function Name:go_at_start
#  * Input: none
#  * Output: none
#  * Logic: will go to suitable place to start corner finding 
#			from.
#  * Example Call: go_at_start()
#**********************************************************

def go_at_start():
	arduino_confirm=False
	mystring=""
	comm_string="@"+"0020"+"0020"+"000"+"000"+"!"
	ser.write(comm_string.encode("ascii"))
	while arduino_confirm == False :
		line_in=ser.readline()
		for char in line_in:
			mystring = mystring + chr(char)
		if mystring == "@done!" :
			arduino_confirm=True
			curr_y=20
			curr_x=20
			curr_z=0

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
	if number == 0 :
		hard_coord_x = 30*no_of_iterations
	elif number == 1 :
		hard_coord_x = 80 
	elif number == 2 :
		hard_coord_y=40

	arduino_confirm=False
	mystring=""
	if corner_finder < 2 :
		comm_string="@"+str(hard_coord_x).zfill(4)+str(curr_y)+str(curr_z)+"000"+"!"
	else : 
		comm_string="@"+str(curr_x)+str(hard_coord_y)+str(curr_z)+"000"+"!"
	ser.write(comm_string.encode("ascii"))
	while arduino_confirm == False :
		line_in=ser.readline()
		for char in line_in:
			mystring = mystring + chr(char)
		if mystring == "@done!" :
			if corner_finder < 2 :
				curr_x = hard_coord_x
			else :
				curr_y = hard_coord_y
			arduino_confirm=True

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
	ret, img = cap.read()
	if cap.isOpened() :
		hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		lower_range=np.array([40,130,130])
		higher_range=np.array([100,255,255])
		mask1 = cv2.inRange(hsv,lower_range,higher_range)
		res = cv2.bitwise_and(img,img, mask=mask1)
		ret,thrshed = cv2.threshold(cv2.cvtColor(res,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
		image,contours,hier = cv2.findContours(thrshed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		areas = [cv2.contourArea(c) for c in contours]
		max_index = np.argmax(areas)
		cnt=contours[max_index]
		peri = cv2.arcLength(cnt, True)
		approx = cv2.approxPolyDP(cnt, 0.006 * peri, True)
		cv2.drawContours(img, [approx], -1, (0,255,0), 5)
		
		if len(approx) == 10 :
			xc,yc=(640,512)
			if corner_finder == 0 :
				point_x=(approx[8][0][0]-xc)*mm_per_pix
				point_y=(approx[8][0][1]-yc)*mm_per_pix
				corner_x=point_x+curr_x
				corner_y=point_y+curr_y
				trough_points.append((corner_x,corner_y))
			elif corner_finder == 1 :
				#point_x=(approx[][0][1]-xc)*mm_per_pix
				#point_y=(approx[][0][1]-yc)*mm_per_pix
				corner_x=point_x+curr_x
				corner_y=point_y+curr_y
				trough_points.append((corner_x,corner_y))
			elif corner_finder == 2 :
				#point_x=(approx[][0][1]-xc)*mm_per_pix
				#point_y=(approx[][0][1]-yc)*mm_per_pix
				corner_x=point_x+curr_x
				corner_y=point_y+curr_y
				trough_points.append((corner_x,corner_y))
			file_string="point"+str(corner_finder)+ ":"+str(corner_x)+" "+str(corner_y)+"\n"
			fhand.write(file_string)	
			corner_finder=corner_finder+1
		no_of_iterations=no_of_iterations+1		
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
#Function Name:get_fourth_point
#  * Input: 3 corners of the trough
#  * Output: 4th corner of the trough
#  * Logic: linear coordinate geometry formulas
#  * Example Call: get_fourth_point(1,2,3,4,5,6)
#**********************************************************
def get_fourth_point(x1,x3,x4,y1,y3,y4):
  m1=(y1-y3)/(x1-x3)
  m2=(y4-y3)/(x4-x3)
  c1=y4-(m1*x4)
  c2=y1-(m2*x1)
  x2=(c2-c1)/(m1-m2)
  y2=(m1*x2)+c1
  return (int(x2),int(y2))

#**********************************************************
#Function Name:get_grids
#  * Input: two points of the line on which grid points 
#			will lie
#  * Output: none 
#  * Logic: linear coordinate geometry formulas
#  * Example Call: get_grids()
#**********************************************************
def get_grids(x1,x2,y1,y2):
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
	x4,y4=trough_points[0]
	x2,y2=trough_points[1]
	x1,y1=trough_points[3]
	x3,y3=get_fourth_point(x1,x2,x3,y1,y2,y3)
	get_grid_points(x1,x2,x3,x4,y1,y2,y3,y4)
    fin = open("grid_points.txt","a")
    temp=""
    plant_no_for_file=1
    for points in grid_p :
    	temp="plant:"+str(plant_no_for_file)+str(points)+"\n"
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
	go_at_start()
	while corner_finder < 3 :
		no_of_iterations=no_of_iterations+1
		hard_distance(corner_finder)
		image_process_for_corner()
	fhand.close()
	create_grid()
		



