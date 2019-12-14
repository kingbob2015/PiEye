import json
from log.logger import Logger, LogLevel


class Config:
    """
    The Config class holds the config data for the application ingested from an external config file

    """
    def __init__(self, config_file=None):
        """
        The constructor for the config class

        @param config_file: The path to the config file to ingest JSON data from
        """
        self.__logger = Logger.get_instance()
        if config_file:
            try:
                with open(config_file) as cFile:
                    self.__config = json.load(cFile)
            except FileNotFoundError:
                self.__logger.log("No config file was found at {}".format(config_file), LogLevel.ERROR)
                __config = {}

        else:
            self.__logger.log("No config file parameter found", LogLevel.ERROR)
            self.__config = {}

    def get_config(self, key):
        """
        Returns the config value for a given key

        @param: key: the key to search for in the config structure

        @return: The value of the config value or None if it didn't exist
        """
        if key in self.__config[key]:
            return self.__config[key]
        else:
            self.__logger.log("The key of {} does not exist in the config".format(key), LogLevel.ERROR)
            return None

    def get_all_config(self):
        """
        Returns the entire dictionary containing the config

        @return: The entire config dictionary
        """
        return self.__config

    def update_config(self, key, value):
        """
        Update a config value in the dictionary or create it if it doesn't exist

        @param: key: the key of the config value
        @param value: the value of the config value
        """
        self.__config[key] = value
