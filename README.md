# pycarmaker

Python class to control, write and read information from CarMaker (https://ipg-automotive.com/).

If you are writing your application in C, use the APO library. Here is an example: https://github.com/gmnvh/pycarmaker/tree/master/examples/C

## How to install

`pip install -e . `

## How to use pycarmaker

```python
from pycarmaker import CarMaker, Quantity

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

# 5 - Subscribe to vehicle speed
# Create a Quantity instance for vehicle speed (vehicle speed is a float type variable)
vehspd = Quantity("Car.v", Quantity.FLOAT)

# Initialize with negative speed to indicate that value was not read
vehspd.data = -1.0

# Subscribe (TCP socket need to be connected)
cm.subscribe(vehspd)

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
c = 5
while(c > 0):
    c = c - 1
    # Read data from carmaker
    cm.read()
    print()
    print("Vehicle speed: " + str(vehspd.data * 3.6) + " km/h")
    print("Simulation status: " + ("Running" if sim_status.data >=
                                   0 else cm.status_dic.get(sim_status.data)))
    time.sleep(1)

```

## How to use VDS:

1. First you need to create a VDS.cfg config file in Movie directory inside your project folder.
    Example cfg:
    ```
    nViews 1
    # First camera
    0 {
    Width 640
    Height 480
    Export {rgb}
    VPtOffset_x 3.1
    VPtOffset_y 0
    VPtOffset_z 1.1
    FrameRate 25
    }
    ```
2. Run a Tes run and open IPGMovie.
3. Launch the following script

```python
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

```

