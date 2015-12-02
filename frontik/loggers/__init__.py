# coding=utf-8

import logging
from logging.handlers import SysLogHandler, WatchedFileHandler
import socket

from tornado.log import LogFormatter
import tornado.options
from tornado.options import options

from frontik.loggers import sentry

LOGGERS = (sentry, )


def bootstrap_app_loggers(app):
    return filter(None, [logger.bootstrap_logger(app) for logger in LOGGERS])


def bootstrap_core_logging():
    """This is a replacement for standard Tornado logging configuration."""

    root_logger = logging.getLogger()
    level = getattr(logging, options.loglevel.upper())
    root_logger.setLevel(logging.NOTSET)

    if options.logfile:
        handler = logging.handlers.WatchedFileHandler(options.logfile)
        handler.setFormatter(logging.Formatter(options.logformat))
        handler.setLevel(level)
        root_logger.addHandler(handler)

    if options.stderr_log:
        handler = logging.StreamHandler()
        handler.setFormatter(
            LogFormatter(
                fmt=tornado.options.options.stderr_format, datefmt=tornado.options.options.stderr_dateformat
            )
        )

        handler.setLevel(level)
        root_logger.addHandler(handler)

    if options.syslog:
        if options.syslog_port is not None:
            syslog_address = (options.syslog_address, options.syslog_port)
        else:
            syslog_address = options.syslog_address

        try:
            syslog_handler = SysLogHandler(
                facility=SysLogHandler.facility_names[options.syslog_facility],
                address=syslog_address
            )
            syslog_handler.setFormatter(logging.Formatter(options.logformat))
            syslog_handler.setLevel(level)
            root_logger.addHandler(syslog_handler)
        except socket.error:
            logging.getLogger('frontik.logging').exception('cannot initialize syslog')

    for logger_name in options.suppressed_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARN)
