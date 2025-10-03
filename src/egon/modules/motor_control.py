from egon.modules.logger import logger
import threading
import pyfirmata2
import time
from egon.modules.console_utils import ConsoleTable


class BufferServo:
    def __init__(self, pin):
        self.pin = pin
        self.current_value = 0
        self._goal_value = 0
        self.running = True
        self.max_seconds_per_degree = 0.002
        self._speed_ratio = 3

        self.th = threading.Thread(target=self.threadloop)
        self.th.start()

    def inch_closer(self):
        if self._goal_value > self.current_value:
            self.current_value += self._speed_ratio
        if self._goal_value < self.current_value:
            self.current_value -= self._speed_ratio

    def threadloop(self):
        while self.running:
            self.inch_closer()
            self.send_msg()
            time.sleep(self.max_seconds_per_degree)

    def send_msg(self):
        self.pin.write(self.current_value)

    def set_goal(self, value=90):
        self._goal_value = max(min(180, value), 0)
        # logger.info(self._goal_value)

    def set_speed(self, value=1):
        self._speed_ratio = max(min(1, value), 0)

    def kill(self):
        self.running = False


class Neck:

    BS = None



    @classmethod
    def update_table(cls):
        if cls.BS is not None:
            return {
                "goal": f"{cls.BS._goal_value: 6.02f}",
                "current": f"{cls.BS.current_value: 6.02f}",
                "speed": f"{cls.BS._speed_ratio: 6.02f}",
            }
        else:
            return {"nothing yet": "nada"}

    @classmethod
    def init_neck(cls):
        logger.info("🦿🙃🦿 neck init")
        cls.PORT = pyfirmata2.Arduino.AUTODETECT
        # cls.PORT = "/dev/ttyACM0"
        logger.info(f"🦿🙃🦿 {cls.PORT}")
        
        cls.board = pyfirmata2.Arduino(cls.PORT)
        cls.pin = cls.board.get_pin("d:9:s")
        cls.BS = BufferServo(cls.pin)
        logger.info("[#55FF88][r]🦿🙃🦿 succesful [/r][/#55FF88]")

    @classmethod
    def move_to(cls, angle, speed_ratio=1):
        cls.BS.set_speed(speed_ratio)
        cls.BS.set_goal(angle)

    @classmethod
    def move_by(cls, angle, speed_ratio=1):
        cls.BS.set_speed(speed_ratio)
        cls.BS.set_goal(cls.BS.current_value + angle)

    @classmethod
    def freeze(cls,*args):
        cls.BS.set_speed(1)
        cls.BS.set_goal(cls.BS.current_value)

    @classmethod
    def make_space(cls, angle=10, speed_ratio=1):
        if cls.BS.current_value < angle:
            cls.move_to(angle,speed_ratio)
        elif cls.BS.current_value > 180 - angle:
            cls.move_to(180 - angle,speed_ratio)



CT = ConsoleTable("🦿🙃🦿 Neck", Neck.update_table, index=4)


