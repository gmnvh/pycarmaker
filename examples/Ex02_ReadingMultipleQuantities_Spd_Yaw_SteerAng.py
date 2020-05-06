import math
import sys
import os
import logging
from types import *
import time

# Include CarMaker
from pycarmaker import CarMaker, Quantity

# Welcome message
print("Ex 02 - Reading multiple quantities - vehicle speed, yaw and steering angle\r\n")

# Enable logging
FORMAT = '[%(levelname)6s] %(module)10s: %(message)s'
logging.basicConfig(format=FORMAT)

# 1 - Open CarMaker with option -cmdport
'''
    For example: on a Windows system with CarMaker 8.0.2 installed on the default
    folder send the command C:\IPG\carmaker\win64-8.0.2\bin\CM.exe -cmdport 16660
'''

# 2 - Start any TesRun

# 3 - Initialize pyCarMaker
IP_ADDRESS = "localhost"
PORT = 16660

cm = CarMaker(IP_ADDRESS, PORT)

# 4 - Connect to CarMaker
cm.connect()

# 5 - Subscribe to quantities

# Create Quantity instances for vehicle speed, yaw and steering angle
vehspd = Quantity("Car.v", Quantity.FLOAT)
caryaw = Quantity("Car.Yaw", Quantity.FLOAT)
steerang = Quantity("Driver.Steer.Ang", Quantity.FLOAT)

# Initialize with negative speed to indicate that value was not read
vehspd.data = -1.0

# Subscribe (TCP socket need to be connected)
cm.subscribe(vehspd)
cm.subscribe(caryaw)
cm.subscribe(steerang)

# 6 - Read all subscribed quantities. In this example, vehicle speed, yaw and steering angle.


c = 10
while(c > 0):
    c = c - 1

    # Read data from carmaker
    cm.read()

    print()
    print("Vehicle speed: " + str(vehspd.data * 3.6) + " km/h")
    print("Vehicle yaw: " + str(round(math.degrees(caryaw.data), 2)))
    print("Steering angle: " + str(round(math.degrees(steerang.data), 2)))
    time.sleep(1)
