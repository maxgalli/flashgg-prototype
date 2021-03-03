from .dataset import Dataset
from .transformation import Cut
from .transformation import Tagger
from .action import NTupleDumper
from .interface import Task
from .run import RunManager
import logging


def setup_logging(logfile, level=logging.INFO):
    from rich.logging import RichHandler
    logger = logging.getLogger("flashgg-logger")

    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(rich_tracebacks=True),
            logging.FileHandler(logfile, "w")
            ]
        )

    return logger
