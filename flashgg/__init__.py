from .dataset import Dataset
from .transformation import Cut
from .transformation import Tagger
from .action import NTupleDumper
from .interface import Task
from .run import RunManager
import logging


def setup_logging(logfile, level=logging.INFO):
    """Setup a logger that uses RichHandler to write the same message both in stdout
    and in a log file called logfile
    """
    from rich.logging import RichHandler
    from rich.console import Console

    logger = logging.getLogger()

    logger.setLevel(level)
    formatter = logging.Formatter("%(message)s")

    stream_handler = RichHandler(show_time=False, rich_tracebacks=True)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = RichHandler(
            show_time=False,
            rich_tracebacks=True,
            console=Console(file=open(logfile, "wt"))
            )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
