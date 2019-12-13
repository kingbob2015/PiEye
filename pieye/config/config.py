import json


class Config:
    def __init__(self, config_file=None):
        if config_file:
            try:
                with open(config_file) as cFile:
                    self.__config = json.load(cFile)
            except FileNotFoundError:
                __config = {}

        else:
            self.__config = {}

    def get_config(self, key):
        # TODO: Add error handling if no key exists
        return self.__config[key]

    def get_all_config(self):
        return self.__config

    def update_config(self, key, value):
        self.__config[key] = value
