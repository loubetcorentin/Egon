from threading import Thread
import logging
from egon.threads.vision_thread import vision_thread
from egon.threads.brain_thread import brain_thread
from egon.threads.console_thread import console_thread
from egon.modules.console_utils import ConsoleTable
from egon.threads.forgetting_thread import fogetting_thread
from egon.threads.hearing_thread import hearing_thread
import time

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    main_table = ConsoleTable("🥚", index=0)
    main_table.d["start"] = time.asctime()

    threads_func = [
        vision_thread,
        brain_thread,
        console_thread,
        fogetting_thread,
        hearing_thread,
    ]

    for func in threads_func:
        t = Thread(target=func, daemon=True)
        t.start()

    # all other threads are killed when this scrip end. So w keep it running until killing manually with ctrl+C
    try:
        while True:
            main_table.d["now"] = time.asctime()
    except KeyboardInterrupt:
        pass
