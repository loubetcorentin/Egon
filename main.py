from threading import Thread
import logging
from threads.vision_thread import vision_thread
from threads.brain_thread import brain_thread
from threads.console_thread import console_thread
from threads.forgetting_thread import fogetting_thread
from modules.short_term_memory import ShortTermMem
import time

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    threads_func = [
        vision_thread,
        brain_thread,
        console_thread,
        fogetting_thread,
    ]

    for func in threads_func:
        t = Thread(target=func, daemon=True)
        t.start()

    # all other threads are killed when this scrip end. So w keep it running until killing manually with ctrl+C
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
