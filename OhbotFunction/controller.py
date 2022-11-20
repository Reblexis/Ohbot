import serial
import serial.tools.list_ports

from OhbotFunction.helpful_functions import checkPort, secure_val, denormalize

HEAD_NOD = 0
HEAD_TURN = 1
EYE_TURN = 2
LID_BLINK = 3
TOP_LIP = 4
BOTTOM_LIP = 5
EYE_TILT = 6
OHBOT_MOTORS = [HEAD_NOD, HEAD_TURN, EYE_TURN, LID_BLINK, TOP_LIP, BOTTOM_LIP, EYE_TILT]

MOTOR_UP_LIMITS = [90, 180, 140, 54, 99, 99, 165, 82]
MOTOR_DOWN_LIMITS = [25, 0, 68, 6, 0, 0, 93, 14]


class OhbotController:
    def __init__(self):
        pass

    def search_connection(self) -> bool:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if checkPort(port):
                self.port = port
                self.ser = serial.Serial(port[0], 19200)
                self.ser.timeout = 0.5
                self.ser.write_timeout = 0.5
                self.ser.flushInput()
                print("Ohbot connected!")
                return True
        return False

    def attach(self, servo: int):
        msg = "a0" + str(servo) + "\n"
        self.ser.write(msg.encode('latin-1'))

    def detach(self, servo: int):
        msg = "d0" + str(servo) + "\n"
        self.ser.write(msg.encode('latin-1'))

    def rotate_head_horizontal(self, horizontal: float, speed: float = 0.5):
        self.attach(HEAD_TURN)
        horizontal = denormalize(secure_val(horizontal, -1, 1), MOTOR_DOWN_LIMITS[HEAD_TURN], MOTOR_UP_LIMITS[HEAD_TURN])
        msg = "m0" + str(HEAD_TURN) + "," + str(horizontal) + "," + str(speed) + "\n"
        self.ser.write(msg.encode('latin-1'))

    def rotate_head_vertical(self, vertical: float, speed: float = 0.5):
        self.attach(HEAD_NOD)
        vertical = denormalize(secure_val(vertical, -1, 1), MOTOR_DOWN_LIMITS[HEAD_NOD], MOTOR_UP_LIMITS[HEAD_NOD])
        msg = "m0" + str(HEAD_NOD) + "," + str(vertical) + "," + str(speed) + "\n"
        self.ser.write(msg.encode('latin-1'))

    def rotate_head_to(self, horizontal: float = 0, vertical: float = 0, speed: float = 0.5):
        speed = denormalize(secure_val(speed, 0, 1), 0, 250, True)
        self.rotate_head_horizontal(horizontal, speed)
        self.rotate_head_vertical(vertical, speed)

    def disconnect(self):
        for motor in OHBOT_MOTORS:
            self.detach(motor)
        self.ser.close()

    def ohbot_motor_reset(self):
        ohbot.reset()
        ohbot.move(ohbot.HEADTURN, 5)
        ohbot.move(ohbot.HEADNOD, 5)
        print("Ohbot motors reset!")

    def ohbot_rotate_head(self, horizontal: float, vertical: float):
        ohbot.move(ohbot.HEADTURN, horizontal)
        ohbot.move(ohbot.HEADNOD, vertical)
        print("Ohbot head moved!")
