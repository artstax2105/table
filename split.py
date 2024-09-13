import numpy as np
import cv2
import time

cap = cv2.VideoCapture('test.mp4')
t = time.time()

i = 0

while (True):
    i += 1
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("frames\\" + str(i) + ".png", gray)
    print(i)
