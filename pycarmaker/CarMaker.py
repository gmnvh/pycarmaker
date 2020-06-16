import socket
import logging
import numpy as np


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
                  -8: "Simulation paused", -10: "Starting application", -11: "Simulink Initialization"}

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
        self.logger.info("Subscribe for quantity " +
                         quantity.name + ": " + str(rsp))
        # TODO Handle error

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

    def DVA_write(self, quantity, value, duration=-1, mode="Abs"):
        """ set the value of a variable using DVAWrite <Name> <Value> <Duration> <Mode> ...
        Parameters
        ----------
        quant : Quantity
            Quantity to set.
        value : Float
            New quantity value
        duration : Float
            Duration in milliseconds
        mode : string
            One of Abs, Off, Fac, AbsRamp, ...; default Abs(olute Value)
        """

        msg = "DVAWrite " + quantity.name + " " + \
            str(value)+" "+str(duration)+" "+mode+"\r"
        self.socket.send(msg.encode())
        rsp = self.socket.recv(200)
        rsp = rsp.decode().split("\r\n\r\n")
        self.logger.info("Write quantity " +
                         quantity.name + ": " + str(rsp))

    def DVA_release(self):
        """ Call this method when you are done using DVA """
        self.send("DVAReleaseQuants\r")

    def send(self, msg):
        """ send the giving message to CarMaker
        Paramters
        ---------
        msg : string
            a string contains the message ending with \ r
        """
        self.socket.send(msg.encode())
        return self.socket.recv(200)


class VDS:
    def __init__(self, ip="localhost", port=2210, log_level=logging.INFO):
        self.logger = logging.getLogger("pycarmaker")
        self.logger.setLevel(log_level)
        self.ip = ip
        self.port = port
        self.socket = None
        self.cameras = []
        self.connected = False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        data = self.socket.recv(64)
        if(data.decode().find("*IPGMovie") != -1):
            self.logger.info("IPG Movie is Connected...")
            self.connected = True

    def read(self):
        """
        Read the streamed images.

        Returns
        -------
        img : numpy array
            a numpy array representing the image

        """
        if not self.connected:
            self.logger.error("Connect first by calling .connect()")
            return
        # Get Image header and fill data
        data = self.socket.recv(64)
        splitdata = data.decode().split(" ")
        imgtype = splitdata[2]
        img_size = splitdata[4]
        data_len = int(splitdata[5])
        imag_h = int(img_size.split('x')[1])
        image_w = int(img_size.split('x')[0])
        lastdata = b''
        size = 0
        while(size != data_len):
            data = self.socket.recv(1024)
            try:
                strdata = data.decode()
                if strdata[0] == '*' and strdata[1] == 'V':
                    splitdata = data.decode().split(" ")
                    imgtype = splitdata[2]
                    img_size = splitdata[4]
                    data_len = int(splitdata[5])
                    imag_h = int(img_size.split('x')[1])
                    image_w = int(img_size.split('x')[0])
                    lastdata = b''
                    size = 0
                    continue
            except:
                pass
            lastdata += data
            size = np.frombuffer(lastdata, dtype=np.uint8).size
        datalist = np.frombuffer(lastdata, dtype=np.uint8)
        if(imgtype == "rgb"):
            img = datalist.reshape((imag_h, image_w, 3))
        elif(imgtype == "grey"):
            img = datalist.reshape((imag_h, image_w))
        else:
            self.logger.error("rgb and gray are supported for now")

        return img
