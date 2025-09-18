from egon.modules.memory import ShortTermMem, LongTermMem
from egon.modules.emotional_state import EmotionalState
from egon.modules.motor_control import Neck

import time
from rich.live import Live
from rich.table import Table
from rich.columns import Columns

from egon.modules.console_utils import ConsoleTableManager


def console_thread():
    with Live(renderable=ConsoleTableManager.display(), refresh_per_second=4) as live:
        while True:
            time.sleep(0.1)

            live.update(ConsoleTableManager.display())


if __name__ == "__main__":  # for debugging
    console_thread()
