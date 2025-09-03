from modules.short_term_memory import ShortTermMem
from modules.emotional_state import EmotionalState

# from modules.logger import logger
import random
import time
from rich.live import Live
from rich.table import Table

mem_table = Table()
mem_table.add_column("sense")
mem_table.add_column("value")


def fill_table():
    mem_table = Table()
    mem_table.add_column("sense")
    mem_table.add_column("value")
    mem_table.add_row("hand", f"{ShortTermMem.get_vision_output()}")
    mem_table.add_row("🧠 SM", f"{EmotionalState.SM.current_state}")
    return mem_table


def console_thread():
    with Live(renderable=fill_table(), refresh_per_second=4) as live:
        while True:
            time.sleep(0.1)

            live.update(fill_table())


if __name__ == "__main__":  # for debugging
    console_thread()
