from threading import Lock
import logging
from enum import Enum
from egon.modules.console_utils import ConsoleTable


class ShortTermMem:
    mem = dict()
    mem_lock = Lock()
    max_activation = 40

    @classmethod
    def set_short_term_mem(cls, x: dict):
        with cls.mem_lock:
            cls.mem = x

    @classmethod
    def add(cls, key,value=1):
        with cls.mem_lock:
            if key in cls.mem.keys():
                if cls.mem[key] < cls.max_activation:
                    cls.mem[key] += value
            else:
                cls.mem[key] = value

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

    @classmethod
    def remove(cls, key):
        with cls.mem_lock:
            if key in cls.mem.keys():
                cls.mem.pop(key)


def update_table_short():
    mem = ShortTermMem.get_short_term_mem()
    d = dict()
    for k, v in mem.items():
        d[k] = f"{v:3d}"
    return d


table = ConsoleTable("🐒🐒 Short Mem", update_table_short, index=2)


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

def update_table_long():
    mem = LongTermMem.get_long_term_mem()
    d = dict()
    for k, v in mem.items():
        d[k] = f"{v:3d}"
    return d
table = ConsoleTable("🦧🦧 Long Mem", update_callback=update_table_long, index=3)
