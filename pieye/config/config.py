import json
from log.logger import Logger, LogLevel

"""
This file contains the Config class which loads in and stores/ updates configuration values for the PiEye application.
"""


class Config:
    """
    The Config class holds the config data for the application ingested from an external config file

    """

    def __init__(self, config_file=None):
        """
        The constructor for the config class

        @param config_file: The path to the config file to ingest JSON data from
        """
        self._logger = Logger.get_instance()
        if config_file:
            try:
                with open(config_file) as cFile:
                    self._config = json.load(cFile)
            except FileNotFoundError:
                self._logger.log("No config file was found at {}".format(config_file), LogLevel.ERROR)
                self._config = {}

        else:
            self._logger.log("No config file parameter found", LogLevel.ERROR)
            self._config = {}

    """
    The string representation of the Config class. Will output all config values.
    """
    def __str__(self):
        ret_string = 'The Configuration Loaded Is: \n'
        for k, v in self.get_all_config().items():
            ret_string += f'{k} : {v} \n'
        return ret_string

    def get_config(self, key):
        """
        Returns the config value for a given key

        @param: key: the key to search for in the config structure

        @return: The value of the config value or None if it didn't exist
        """
        if key in self._config.keys():
            return self._config[key]
        else:
            self._logger.log("The key of {} does not exist in the config".format(key), LogLevel.ERROR)
            return None

    def get_all_config(self):
        """
        Returns the entire dictionary containing the config

        @return: The entire config dictionary
        """
        return self._config

    def update_config(self, key, value):
        """
        Update a config value in the dictionary or create it if it doesn't exist

        @param: key: the key of the config value
        @param value: the value of the config value
        """
        self._config[key] = value
