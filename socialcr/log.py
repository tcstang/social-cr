#!/usr/bin/env python

import logging
import logging.config
import logging.handlers
from git import *

class LogManager:
    def __init__(self, name):
        self.logger = SimpleLoggerFactory.get_logger(name)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)


class LogFactory:
    """ Abstract factory for creating loggers """

    def get_logger(self, name):
        raise NotImplementedError( "Should have implemented this" )

class SimpleLoggerFactory(LogFactory):
    """ A simple, typical, static, logger """

    def get_logger(self, name):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler()
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger
