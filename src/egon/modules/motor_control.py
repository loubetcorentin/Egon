from egon.modules.logger import logger
import threading
import pyfirmata2
import time


class BufferServo:
    def __init__(self, pin):
        self.pin = pin
        self.current_value = 0
        self.goal_value = 0
        self.running = True
        self.max_seconds_per_degree = 0.005
        self.speed_ratio = 1

        self.th = threading.Thread(target=self.threadloop)
        self.th.start()
        
        
    def inch_closer(self):
        if self.goal_value > self.current_value:
            self.current_value += self.speed_ratio
        if self.goal_value < self.current_value:
            self.current_value -= self.speed_ratio

    def threadloop(self):
        while self.running:
            self.inch_closer()
            self.send_msg()
            time.sleep(self.max_seconds_per_degree)

    def send_msg(self):
        self.pin.write(self.current_value)

    def write(self, value, speed_ratio=1):
        """This is the function to send orders to the motor

        Args:
            value (_type_): _description_
        """
        self.goal_value = value
        self.speed_ratio = speed_ratio

    def kill(self):
        self.running = False


class Neck:

    @classmethod
    def init_neck(cls):
        logger.info("🦿🙃🦿 neck init")
        cls.PORT = pyfirmata2.Arduino.AUTODETECT
        cls.board = pyfirmata2.Arduino(cls.PORT)
        cls.pin = cls.board.get_pin("d:9:s")
        cls.BS = BufferServo(cls.pin)
        logger.info("[#55FF88][r]🦿🙃🦿 succesful [/r][/#55FF88]")

    @classmethod
    def move_to(cls, angle, speed_ratio):
        cls.BS.write(angle, speed_ratio)

    @classmethod
    def move_by(cls, angle, speed_ratio):
        cls.BS.write(cls.BS.current_value+angle, speed_ratio)


Neck.init_neck()


def act_no():
    Neck.move_to(90, speed_ratio=1)
    time.sleep(0.4)
    Neck.move_to(45, speed_ratio=0.3)
    time.sleep(0.4)
    Neck.move_to(135, speed_ratio=0.3)
    time.sleep(0.4)
    Neck.move_to(45, speed_ratio=0.3)
    time.sleep(0.4)
    Neck.move_to(135, speed_ratio=0.3)
    time.sleep(0.4)
    Neck.move_to(90, speed_ratio=1)
