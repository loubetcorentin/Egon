from threading import Lock
import logging
from enum import Enum

class ShortTermMem:
    VISION_OUTPUT = dict()
    STATE_LOCK = Lock()

    @classmethod
    def set_vision_output(cls, x: dict):
        with cls.STATE_LOCK:
            cls.VISION_OUTPUT = x

    @classmethod
    def get_vision_output(cls):
        x = None
        with cls.STATE_LOCK:
            x = cls.VISION_OUTPUT
        return x
