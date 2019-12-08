import json


class Config:
    def __init__(self, configFile):
        with open(configFile) as cFile:
            self.__config = json.load(cFile)

    def get_config(self, key):
        # TODO: Add error handling if no key exists
        return self.__config[key]

    def get_all_config(self):
        return self.__config