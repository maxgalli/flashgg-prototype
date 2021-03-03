import logging
logger = logging.getLogger(__name__)


class EmptyListError(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        logger.fatal(msg)

    def __str__(self):
        return self.msg
