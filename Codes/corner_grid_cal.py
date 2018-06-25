#**********************************************************
#Function Name:
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
global hard_dist_x
global hard_dist_y
global pix_per_mm
global no_of_iterations

#************Initialization*************

arduino_confirm = False
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)
time.sleep(2)
comm_string=""
curr_x=0
curr_y=0
curr_z=0
corner_finder=0
mm_per_pix=0.364996557
pix_per_mm=2.739751871
no_of_iterations = 0
hard_dist_x=0
hard_dist_y=0

#**************************************

#************Functions******************
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
	if number is 0 :
		hard_dist = 30*no_of_iterations
	elif number is 1 :
		hard_dist = 80 - ((no_of_iterations-1)*30)
def find_corners():
	while corner_finder < 4
		no_of_iterations=no_of_iterations+1
		hard_distance(corner_finder)
		image_process_for_corner()
		



