from egon.modules.memory import ShortTermMem, LongTermMem
from egon.modules.logger import logger

# from modules.logger import logger
import random
import time


def random_forget():
    if random.random() < 0.95:

        mem = ShortTermMem.get_short_term_mem()
        for key in list(mem.keys()):
            ShortTermMem.remove_one(key)

        logger.debug("🐒 forgot")
    if random.random() < 0.05:

        mem = LongTermMem.get_long_term_mem()
        for key in list(mem.keys()):
            LongTermMem.remove_one(key)

        logger.debug("🦧 BIG forgot")


def forgetting_thread():
    while True:
        time.sleep(0.2)
        random_forget()


if __name__ == "__main__":  # for debugging
    forgetting_thread()
