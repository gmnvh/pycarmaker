import socket
import logging

class Quantity():
    FLOAT = 1.0
    INT = 1

    def __init__(self, name, q_type, command=False):
        self.name = name
        self.type = q_type
        self.command = command
        self.data = None
        
        if command == True:
            self.read_msg = self.name + "\r"
        else:
            self.read_msg = "expr {$Qu(" + self.name + ")}\r"

class CarMaker():
    status_dic = {-1: "Preprocessing", -2: "Idle", -3: "Postprocessing", -4: "Model Check",
                  -5: "Driver Adaption", -6: "FATAL ERROR", -7: "Waiting for License",
                  -8: "Simulation paused", -10: "Starting application", -11:"Simulink Initialization"}

    def __init__(self, ip, port, log_level=logging.INFO):
        self.logger = logging.getLogger("pycarmaker")
        self.logger.setLevel(log_level)

        self.ip = ip
        self.port = port

        self.socket = None
        self.quantities = []

        self.logger.debug("pycarmaker init completed")

    def connect(self):
        # Open the TCP / IP port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the CM TCP / IP port 16660 on localhost
        self.socket.connect((self.ip, self.port))
        self.logger.info("TCP socket connected")

    def subscribe(self, quantity):
        self.quantities.append(quantity)

        if quantity.command == True:
            self.logger.info("Subscribe for command " + quantity.name + ": OK")
            return

        # Create message to subscribe to quantities with all quantities
        # previous subscribed
        msg = ""
        for q in self.quantities:
            if msg is "":
                msg = q.name
            else:
                msg += " " + q.name
        msg = "QuantSubscribe {" + msg + "}\r"
        self.logger.debug(msg)

        if (self.socket == None):
            self.logger.error("Not connected")
            return
        
        self.socket.send(msg.encode())
        rsp = self.socket.recv(200)
        rsp = rsp.decode().split("\r\n\r\n")
        self.logger.info("Subscribe for quantity " + quantity.name + ": " + str(rsp))
        #TODO Handle error

    def read(self):
    
        # By IPG recommendation, read one quantity at a time.
        for quantity in self.quantities:
            self.socket.send(quantity.read_msg.encode())
            str_rx = self.socket.recv(300).decode()
            rx_list = str_rx.split("\r\n\r\n")
            self.logger.debug(rx_list)

            if (len(rx_list) != 2):
                self.logger.error("Wrong read")
                return

            if type(quantity.type) == type(Quantity.FLOAT):
                quantity.data = float(rx_list[0][1:])
            elif type(quantity.type) == type(Quantity.INT):
                quantity.data = int(rx_list[0][1:])
            else:
                self.logger.error("Unknwon type")