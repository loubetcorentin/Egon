from egon.modules.memory import ShortTermMem, LongTermMem
from egon.modules.emotional_state import EmotionalState
from egon.modules.motor_control import Neck

# from modules.logger import logger
import random
import time
from rich.live import Live
from rich.table import Table
from rich.columns import Columns
from rich.layout import Layout


def short_mem_table():
    t = Table()
    t.add_column("🐒🐒 Short Mem")
    for key, value in ShortTermMem.get_short_term_mem().items():
        t.add_row(key, f"{value:3d}")
    return t


def long_mem_table():
    t = Table()
    t.add_column("🦧🦧 Long Mem")
    for key, value in LongTermMem.get_long_term_mem().items():
        t.add_row(key, f"{value:3d}")
    return t


def neck_table():
    t = Table()
    t.add_column("🦿🙃🦿 neck")
    for key, value in Neck.read_pos().items():
        t.add_row(key, f"{value:2f}")
    return t


def brain_table():
    t = Table()
    t.add_column("🧠🧠🧠🧠 brain")
    t.add_row("Emotional State", f"{str(EmotionalState.SM.current_state):^15}")

    return t


def coco():
    c = Columns([brain_table(), short_mem_table(), long_mem_table(), neck_table()])
    return c


def console_thread():
    with Live(renderable=coco(), refresh_per_second=4) as live:
        while True:
            time.sleep(0.1)

            live.update(coco())


if __name__ == "__main__":  # for debugging
    console_thread()
