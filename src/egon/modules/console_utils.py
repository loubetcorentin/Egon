from rich.table import Table
from rich.columns import Columns


class ConsoleTableManager:

    tables_dict = dict()

    @classmethod
    def register(cls, td, index):
        cls.tables_dict[f"{index} {td.title}"] = td


    @classmethod
    def display_table(cls, table):
        if table.update_callback is not None:
            table.d = table.update_callback().copy()
        t = Table()
        t.add_column(table.title)
        for key, value in table.d.items():
            t.add_row(key, value)
        return t

    @classmethod
    def display(cls):
        return Columns([cls.display_table(kt[1]) for kt in cls.tables_dict.items()])


class ConsoleTable:
    def __init__(self, title: str, update_callback=None, index=0):
        self.d = dict()
        self.title = f"{index} {title}"
        self.update_callback = update_callback
        ConsoleTableManager.register(self, index)
