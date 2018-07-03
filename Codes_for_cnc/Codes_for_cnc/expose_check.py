import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)
cap.set(15,1.9)
ret, frame=cap.read()
ret, frame = cap.read()
roi = cv2.resize(frame,(800,800))
cv2.imwrite("frame.jpg",roi)