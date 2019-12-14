import os
import enum

# TODO: Error handling for file stuff

class LogLevel(enum.Enum):
    INFO = 1
    WARN = 2
    ERROR = 3

class Logger:
    __instance, __file, __logLevel = None, None, None

    @staticmethod
    def get_instance(log_level=LogLevel.INFO, log_file=os.path.dirname(__file__) + "/../log.txt"):
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
        if log_level.value >= Logger.__logLevel.value:
            with open(self.__file, "a") as file:
                file.write(log_message + "\n")
