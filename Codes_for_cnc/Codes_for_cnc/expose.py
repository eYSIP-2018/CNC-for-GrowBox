#import cv2
#import numpy as np

#cap = cv2.VideoCapture(0)
#cap.set(3,1280)
#cap.set(4,1024)
#cap.set(15,1)
#ret, frame=cap.read()
#ret, frame = cap.read()
#roi = cv2.resize(frame,(800,800))
#cv2.imwrite("frame.jpg",roi)
import cv2
import numpy as np
import math

#mm_per_pix 0.364996557

def get_ratio_points(x1,x2,y1,y2,k1,k2):
  x0 = ((x1*k2)+(x2*k1))/(k1+k2)
  y0 = ((y1*k2)+(y2*k1))/(k1+k2)
  return int(x0),int(y0)
def cal_distance(x1,x2,x3,x4,y1,y2,y3,y4):
	xc,yc=(640,512)
	xt,yt=get_ratio_points(x1,x2,y1,y2,1,1)
	xd,yd=get_ratio_points(x4,x3,y4,y3,1,1)
	xs,ys=get_ratio_points(xt,xd,yt,yd,1,1)
	cv2.circle(img,(xs,ys),5,(0,0,255),-1)
	distance = math.sqrt(math.pow(xc-xs,2)+math.pow(yc-ys,2))
	mm_per_pix=0.364996557;
	print(distance*mm_per_pix)

	cv2.line(img, (int(xc),int(yc)), (xs,ys), (255,0,0), 2) 


img=cv2.imread("img00.jpg")

hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
lower_range=np.array([172,65,65])
higher_range=np.array([180,255,255])
mask1 = cv2.inRange(hsv,lower_range,higher_range)
res = cv2.bitwise_and(img,img, mask=mask1)
ret,thrshed = cv2.threshold(cv2.cvtColor(res,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
image,contours,hier = cv2.findContours(thrshed,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

#print(areas[max_index]) #15000 area 

#print(box)
#cv2.circle(img,(x4,y4),5,(0,0,255),-1)
area = 0
for cnt in contours :
	area = cv2.contourArea(cnt)
	
	if area>1000 :
            
            print(area)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            x4,y4=box[0]
            x3,y3=box[1]
            x1,y1=box[2]
            x2,y2=box[3]
            img = cv2.drawContours(img,[box],-1,(0,0,255),2)
#cal_distance(x1,x2,x3,x4,y1,y2,y3,y4)
roi=cv2.resize(img,(600,600))
cv2.imshow("frame",roi)
cv2.waitKey(0)
