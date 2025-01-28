import numpy as np
import time
from time import sleep
from tkinter import *
from tkinter import messagebox
import threading
import os
 
 
def detect(): 
    delay=20*1   ###for 1 minutes delay 
    close_time=time.time()+delay
    cap = cv2.VideoCapture(0)
 
 
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
 
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 900:
                print("in frame")
                continue
            messagebox.showinfo("showinfo", "You are caught")
            os._exit(1)           
        cv2.imshow("feed", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()
 
        if time.time()>close_time:
            break
 
    cv2.destroyAllWindows()
    cap.release()
    main_loop_func()
