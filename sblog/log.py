"""
sblog.logging
From flask.logging
"""

from __future__ import absolute_import

from logging import getLogger, StreamHandler, Formatter, getLoggerClass, DEBUG


def create_logger(app):
    Loggoer = getLoggerClass()

    class DebugLogger(Loggoer):
        def getEffectiveLevel(self):
            if self.level == 0 and app.debug:
                return DEBUG

            return Loggoer.getEffectiveLevel(self)

    class DebugHandler(StreamHandler):
        def emit(self, record):
            StreamHandler.emit(self, record) if app.debug else None


    handler = DebugHandler()
    handler.setLevel(DEBUG)
    handler.setFormatter(Formatter(app.debug_log_format))
    logger = getLogger(app.logger_name)

    del logger.handlers[:]
    logger.__class__ = DebugLogger
    logger.addHandler(handler)
    return logger