import sys
import os
import logging
from types import *
import time
import cv2
from pycarmaker import VDS

# initalize VDS
vds = VDS()
# Connect
vds.connect()
# Read Images
while(True):
    # Capture frame-by-frame
    frame = vds.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # Display the resulting frame
    cv2.imshow('Frame', frame)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
