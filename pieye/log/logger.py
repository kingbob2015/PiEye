import os

# TODO: Error handling for file stuff


class Logger:
    __instance = None
    __file = os.path.dirname(__file__) + "/../log.txt"

    @staticmethod
    def get_instance():
        if Logger.__instance is None:
            Logger()
        return Logger.__instance

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception("This class is a singleton and one is created")
        else:
            with open(self.__file, "w") as file:
                file.write("PiEye Log\n---------------------\n")
            Logger.__instance = self

    def log(self, log_message):
        with open(self.__file, "a") as file:
            file.write(log_message + "\n")