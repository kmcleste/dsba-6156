import logging
import pathlib

from rich.logging import RichHandler

# TODO: Create logger class
# TODO: Convert file handler to use json logging
# TODO: Create log directory if not exists

logger = logging.getLogger(__name__)

# the handler determines where the logs go: stdout/file
shell_handler = RichHandler()
file_handler = logging.FileHandler(pathlib.Path("logs", "debug.log"))

logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# the formatter determines what our logs will look like
fmt_shell = "%(message)s"
fmt_file = (
    "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
)

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

# here we hook everything together
shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

# ensures we do not print duplicate logs
if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(shell_handler)
logger.addHandler(file_handler)
