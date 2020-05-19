from pycarmaker import CarMaker, Quantity
import time

# 1 - Initialize pyCarMaker
IP_ADDRESS = "localhost"
PORT = 16660
cm = CarMaker(IP_ADDRESS, PORT)

# 2 - Connect to CarMaker
cm.connect()

# 3 - Create a Quantity
qbrake = Quantity("DM.Brake", Quantity.FLOAT)

# 4 - Press the Brake
cm.DVAWrite(qbrake, 1)

# 5 - wait for 5 seconds
time.sleep(5)

# 6 - Release the Brake
cm.DVAWrite(qbrake, 0)
