from egon.modules.short_term_memory import ShortTermMem
from egon.modules.logger import logger
# from modules.logger import logger
import random
import time

def random_forget():
    if random.random()<0.2:
        ShortTermMem.set_vision_output(dict())
        logger.info("🐒 forgot")

def fogetting_thread():
    while True:
        time.sleep(1)
        random_forget()
        


if __name__ == "__main__":  # for debugging
    fogetting_thread()
