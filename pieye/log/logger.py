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
    __instance, __file, __logLevel = None, None, None

    @staticmethod
    def get_instance(log_level=LogLevel.INFO, log_file=os.path.dirname(__file__) + "/../log.txt"):
        """
        Gets the instance of Logger if it has been instantiated or creates one

        @param: log_level: the level of logging, takes from the enum of LogLevel
        @param: log_file: the file to log to

        @return: The instance of the singleton Logger
        """
        if Logger.__instance is None:
            Logger(log_level, log_file)
        return Logger.__instance

    def __init__(self, log_level, log_file):
        if Logger.__instance is not None:
            raise Exception("This class is a singleton and one is created")
        else:
            Logger.__file = log_file
            with open(self.__file, "w") as file:
                file.write("PiEye Log\n---------------------\n")
            Logger.__logLevel = log_level
            Logger.__instance = self

    def log(self, log_message, log_level):
        """
        Logs a message

        @param: log_message: the message to log to the file that the Logger was instantiated with
        @param log_level: the level that the log message is logging for from the enum of LogLevel
        """
        if log_level.value >= Logger.__logLevel.value:
            with open(self.__file, "a") as file:
                file.write(log_message + "\n")
