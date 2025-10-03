from threading import Thread
import logging
from egon.threads.vision_thread import vision_thread
from egon.threads.brain_thread import brain_thread
from egon.threads.console_thread import console_thread
from egon.modules.console_utils import ConsoleTable
from egon.threads.forgetting_thread import forgetting_thread
from egon.threads.hearing_thread import hearing_thread
from egon.threads.neck_thread import neck_thread
import time

logging.basicConfig(level=logging.INFO)

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

    thread_list: list[Thread] = []
    for func in threads_func:
        t = Thread(target=func, daemon=True)
        t.start()
        thread_list.append(t)

    # all other threads are killed when this scrip end. So w keep it running until killing manually with ctrl+C
    try:
        prev_isalive = dict()
        for t in thread_list:
            prev_isalive[t] = True

        while True:

            now_str = time.strftime("%x %X", time.localtime())
            main_table.d["now"] = now_str
            for t in thread_list:
                alive = t.is_alive()
                func = t.name

                if alive:
                    main_table.d[func.split("-")[1]] = "💚"
                else:
                    if prev_isalive[t]:
                        main_table.d[func.split("-")[1]] = f"💀 {now_str}"
                        prev_isalive[t] = False

    except KeyboardInterrupt:
        pass
