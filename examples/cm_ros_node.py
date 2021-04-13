#!/usr/bin/env python
import sys
import os
import logging
from types import *
import time
from pycarmaker import CarMaker, Quantity
import rospy
from std_msgs.msg import Float32
FORMAT = '[%(levelname)6s] %(module)10s: %(message)s'
logging.basicConfig(format=FORMAT)

if __name__ == "__main__":
    try:
        IP_ADDRESS = "localhost"
        PORT = 16660
        cm = CarMaker(IP_ADDRESS, PORT)
        cm.connect()
        car_speed = Quantity("Car.v", Quantity.FLOAT)
        car_yaw = Quantity("Car.Yaw", Quantity.FLOAT)
        driver_steer = Quantity("Driver.Steer.Ang", Quantity.FLOAT)
        # Initialize with negative speed to indicate that value was not read
        car_speed.data = -1.0
        car_yaw.data = -1.0
        driver_steer.data = -1.0
        # Subscribe (TCP socket need to be connected)
        cm.subscribe(car_speed)
        cm.subscribe(car_yaw)
        cm.subscribe(driver_steer)

        # Let's also read the simulation status (simulation status is not a quantity but a command
        # so the command parameter must be set to True)
        sim_status = Quantity("SimStatus", Quantity.INT, True)
        cm.subscribe(sim_status)

        # 6 - Read all subscribed quantities. In this example, vehicle speed and simulation status

        # For some reason, the first two reads will be incomplete and must be ignored
        # You will see 2 log errors like this: [ ERROR]   CarMaker: Wrong read
        cm.read()
        cm.read()
        time.sleep(0.1)
        # ROS Publishers
        rospy.init_node('cmros', anonymous=True)
        speedpub = rospy.Publisher(
            '/cmros/car/speed', Float32, queue_size=10)
        yawpub = rospy.Publisher(
            '/cmros/car/yaw', Float32, queue_size=10)
        steerpub = rospy.Publisher(
            '/cmros/driver/steer/ang', Float32, queue_size=10)
        # Publishing Rate.
        rate = rospy.Rate(30)  # 30hz
        print("Connecting")
        while not rospy.is_shutdown():
            cm.read()
            print()
            print("Car speed: " + str(car_speed.data * 3.6) + " km/h")
            print("Car Yaw: " + str(car_yaw.data))
            print("Steering Angle: " + str(driver_steer.data))
            print("Simulation status: " + ("Running" if sim_status.data >=
                                           0 else cm.status_dic.get(sim_status.data)))
            floatmsg = Float32()
            floatmsg.data = car_speed.data * 3.6
            speedpub.publish(floatmsg)
            floatmsg.data = car_yaw.data
            yawpub.publish(floatmsg)
            floatmsg.data = driver_steer.data
            steerpub.publish(floatmsg)
            rate.sleep()
    except rospy.ROSInterruptException:
        print("Shutting Down !. GoodBye")
    except Exception as e:
        print(e)
        print("Can't connect. Make sure CarMaker is running on port 16660")
        print("Run it first /opt/ipg/carmaker/linux64-8.1.1/bin/CM -cmdport 16660 ")
