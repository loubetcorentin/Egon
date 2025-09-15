from modules.logger import logger
import threading
import pyfirmata2
import time

class BufferServo():
    def __init__(self, pin):
        self.pin = pin
        self.current_value = 0
        self.goal_value = 0
        self.th = threading.Thread(target=self.threadloop)
        self.running=True
        self.th.start()
        self.max_seconds_per_degree = 0.005
        self.speed_ratio = 1
        
    def inch_closer(self):
        if self.goal_value> self.current_value:
            self.current_value +=self.speed_ratio
        if self.goal_value< self.current_value:
            self.current_value -=self.speed_ratio
        
    def threadloop(self):
        while self.running:
            self.inch_closer()
            self.send_msg()
            time.sleep(self.max_seconds_per_degree)
        
    def send_msg(self):
        self.pin.write(self.current_value)
        
    def write(self,value,speed_ratio  =1):
        """This is the function to send orders to the motor

        Args:
            value (_type_): _description_
        """
        self.goal_value = value
        self.speed_ratio = speed_ratio
        
    def kill(self):
        self.running = False
    
    
class Neck:
    PORT =  pyfirmata2.Arduino.AUTODETECT
    board = pyfirmata2.Arduino(PORT)
    pp = board.get_pin("d:9:s")
    BS = BufferServo(pp)
    logger.info("🦿🙃🦿")
    
    @classmethod
    def move_to(cls,angle,speed_ratio):
        cls.BS.write(angle, speed_ratio)
    
      
