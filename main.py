from threading import Thread
import logging
from typing import Callable
from egon.modules.logger import logger
from egon.threads.vision_thread import vision_thread
from egon.threads.brain_thread import brain_thread
from egon.threads.console_thread import console_thread
from egon.modules.console_utils import ConsoleTable
from egon.threads.forgetting_thread import forgetting_thread
from egon.threads.hearing_thread import hearing_thread
from egon.threads.neck_thread import neck_thread
import time

logging.basicConfig(level=logging.INFO)

prev_isalive = dict()
thread_list: list[[Thread,Callable]] = []

def start_thread(func):
    t = Thread(target=func, daemon=True)
    t.start()
    logger.info(f"started thread {t}")
    thread_list.append([t,func])
    prev_isalive[t] = True

if __name__ == "__main__":

    main_table = ConsoleTable("🥚", index=0)
    main_table.d["start"] = time.strftime("%x %X", time.localtime())

    threads_func = [
        vision_thread,
        brain_thread,
        console_thread,
        forgetting_thread,
        hearing_thread,
        neck_thread,
    ]

    for func in threads_func:
        start_thread(func)
        
    
    try:

        while True: # all other threads are killed when this scrip end. So w keep it running until killing manually with ctrl+C

            now_str = time.strftime("%x %X", time.localtime())
            main_table.d["now"] = now_str
            for t_fn in thread_list.copy():
                t,fn = t_fn
                alive = t.is_alive()
                func_name = t.name

                if alive:
                    main_table.d[func_name.split("-")[1]] = f"💚 "
                else:
                    if prev_isalive[t]:
                        main_table.d[func_name.split("-")[1]] = f"💀 {now_str}"
                        prev_isalive[t] = False
                        logger.warning(f"💀 {t} has just died")
                        logger.info(f" restarting {t} ")

                        start_thread(fn)
  

    except KeyboardInterrupt:
        pass
