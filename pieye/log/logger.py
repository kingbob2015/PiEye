"""
This file contains the Logger class that is a singleton for logging to a log file and the LogLevel class enum
for INFO, WARN, and ERROR level logging that controls what is logged from log messages.
"""

import os
import enum


class LogLevel(enum.Enum):
    """
    The LogLevel class contains the enums for log levels. INFO, WARN, or ERROR
    """
    INFO = 1
    WARN = 2
    ERROR = 3


class Logger:
    """
    The Logger class  singleton that can take parameters for log level from the LogLevel class and log file path
    Only access the Logger class via get_instance
    """
    _instance, _file, _logLevel = None, None, None

    @staticmethod
    def get_instance(log_level=LogLevel.INFO, log_file=os.path.dirname(__file__) + "/../log.txt"):
        """
        Gets the instance of Logger if it has been instantiated or creates one

        @param: log_level: the level of logging, takes from the enum of LogLevel
        @param: log_file: the file to log to

        @return: The instance of the singleton Logger
        """
        if Logger._instance is None:
            Logger(log_level, log_file)
        return Logger._instance

    def __init__(self, log_level, log_file):
        if Logger._instance is not None:
            raise Exception("This class is a singleton and one is created")
        else:
            Logger._file = log_file
            with open(self._file, "w") as file:
                file.write("PiEye Log\n---------------------\n")
            Logger._logLevel = log_level
            Logger._instance = self

    def log(self, log_message, log_level):
        """
        Logs a message

        @param: log_message: the message to log to the file that the Logger was instantiated with
        @param log_level: the level that the log message is logging for from the enum of LogLevel
        """
        if log_level.value >= Logger._logLevel.value:
            with open(self._file, "a") as file:
                file.write(log_message + "\n")
