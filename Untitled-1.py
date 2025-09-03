import time
from rich import print
from rich.live import Live
from rich.table import Table

table = Table()
table.add_column("Row ID")
table.add_column("Description")
table.add_column("Level")

row = 0
with Live(renderable=table, refresh_per_second=4) as live:  # update 4 times a second to feel fluid
    while True:
        row += 1
        print(f"Working on row #{row}")
        time.sleep(0.4)
        if row < 8:
            table.add_row(f"{row}", f"description {row}", "[red]ERROR")
