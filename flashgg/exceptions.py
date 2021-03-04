import logging
logger = logging.getLogger(__name__)


class EmptyListError(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        logger.fatal(self.msg)

    def __str__(self):
        return self.msg


class FormatNotSupported(Exception):
    def __init__(self, supported_formats):
        self.msg = "Format not supported. Supported formats are: {}".format(supported_formats)
        logger.fatal(self.msg)

    def __str__(self):
        return self.msg
