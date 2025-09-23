"""This module handles all logging for this project.
All logs are displayed in color in thd console and stored in the `egon.log` file.
I use the Rich library for colored outputs.
"""

import logging
from rich import print

from rich.text import Text


class RichHandler(
    logging.StreamHandler
):  # uses rich print in console to get access to colors and stuff
    def emit(self, record):
        txt = self.format(record=record)
        print(txt)


class PoorFormater(logging.Formatter):  # removes rich stuff for file log
    def formatMessage(self, record):
        return "".join(Text.from_markup(record.getMessage())._text)


class VeryRichFormater(logging.Formatter):
    def formatMessage(self, record):
        return super().formatMessage(record)


file_handler = logging.FileHandler("egon.log", encoding="utf-8", mode="a")
file_handler.setFormatter(PoorFormater())

console_handler = RichHandler()
formatter = logging.Formatter(
    "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)

# console_handler.setFormatter(VeryRichFormater())
console_handler.setFormatter(formatter)


logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])

logger = logging.getLogger()  # the thing you should log with.


logger.info("[#55FF88][r]🐒🐒🐒 logger is setup [/r][/#55FF88]")
