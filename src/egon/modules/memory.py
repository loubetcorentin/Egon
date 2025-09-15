from threading import Lock
import logging
from enum import Enum


class ShortTermMem:
    mem = dict()
    mem_lock = Lock()

    @classmethod
    def set_short_term_mem(cls, x: dict):
        with cls.mem_lock:
            cls.mem = x

    @classmethod
    def add(cls, key):
        with cls.mem_lock:
            if key in cls.mem.keys():
                if cls.mem[key] < 100:
                    cls.mem[key] += 1
            else:
                cls.mem[key] = 1

    @classmethod
    def get_short_term_mem(cls):
        x = None
        with cls.mem_lock:
            x = cls.mem
        return x

    @classmethod
    def remove_one(cls, key):
        with cls.mem_lock:
            if key in cls.mem.keys():
                if cls.mem[key] > 0:
                    cls.mem[key] -= 1
                else:
                    cls.mem.pop(key)


class LongTermMem:
    mem = dict()
    mem_lock = Lock()

    @classmethod
    def remove_one(cls, key):
        with cls.mem_lock:
            if key in cls.mem.keys():
                if cls.mem[key] > 0:
                    cls.mem[key] -= 1
                else:
                    cls.mem.pop(key)

    @classmethod
    def set_long_term_mem(cls, x: dict):
        with cls.mem_lock:
            cls.mem = x

    @classmethod
    def add(cls, key):
        with cls.mem_lock:
            cls.mem[key] = 100

    @classmethod
    def get_long_term_mem(cls):
        x = None
        with cls.mem_lock:
            x = cls.mem
        return x
