import time
import socket


# Computer on which the TCg / IP port is opened
TCP_IP = 'localhost'
# Port number
TCP_PORT = 16660 
BUFFER_SIZE = 10240

# Open the TCP / IP port in Python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the CM TCP / IP port 16660 on localhost
s.connect((TCP_IP, TCP_PORT))

MESSAGE = "QuantSubscribe {Time Car.v Car.tx Car.ty}\r"
s.send(MESSAGE.encode())
s_string_val = s.recv(10)


MSG_VEH_POS_X = "expr {$Qu(Car.tx)}\r"
MSG_VEH_POS_Y = "expr {$Qu(Car.ty)}\r"
MSG_VEH_SPEED = "expr {$Qu(Car.v)*3.6}\r"
MSG_SIM_STATUS = "SimStatus\r"

MSG = MSG_SIM_STATUS + MSG_VEH_SPEED + MSG_VEH_POS_X + MSG_VEH_POS_Y
print(MSG.encode())

# Try 1
s.send(MSG.encode())
str_rx = s.recv(200).decode()
rx_list = str_rx.split("\r\n\r\n")
print('Try 1')
print(rx_list)

time.sleep(0.1)

# Try 2
s.send(MSG.encode())
str_rx = s.recv(200).decode()
rx_list = str_rx.split("\r\n\r\n")
print('Try 2')
print(rx_list)

time.sleep(0.1)

# Try 3
s.send(MSG.encode())
str_rx = s.recv(200).decode()
rx_list = str_rx.split("\r\n\r\n")
print('Try 3')
print(rx_list)

time.sleep(0.1)

# Try 4
s.send(MSG.encode())
str_rx = s.recv(200).decode()
rx_list = str_rx.split("\r\n\r\n")
print('Try 4')
print(rx_list)