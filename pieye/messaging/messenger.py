from abc import ABC, abstractmethod
import smtplib
from config.config import Config
from log.logger import Logger, LogLevel

"""
This file contains classes for messaging people
"""


"""
The Messenger class is an abstract base class to be implemented by child Messenger classes
"""


class Messenger(ABC):

    """
    The constructor of messenger classes takes a config which is a Config object
    """
    def __init__(self, config: Config):
        self._configObject = config
        self._logger = Logger.get_instance()
        self._messenger_dict = self._configObject.get_config("messaging")
        self._server_connection = None
        if self._messenger_dict:
            self._connect_server()
        else:
            self._logger.log('No messenger_login dict found in config object, messaging system will not work',
                             LogLevel.ERROR)
            self._messenger_dict = {}

    """
    The destructor of messenger classes to close server connection
    """
    def __del__(self):
        self._server_connection.close()

    """
    Instance method to try to connect to the messaging server.
    """
    def _connect_server(self):
        if self._server_connection:
            self._server_connection.close()
        self._server_connection = None
        try:
            self._server_connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            self._server_connection.ehlo()
            self._server_connection.login(self._messenger_dict["messenger_login"]["email_address"],
                                          self._messenger_dict["messenger_login"]["email_password"])
        except KeyError:
            self._logger.log('The messenger_login dict did not contain email_address and/or email_password',
                             LogLevel.ERROR)
        except Exception as e:
            self._logger.log(f'The exception {e} was triggered', LogLevel.ERROR)

    """
    This function is an abstract function to be implemented by child classes to send a message
    
    @param: name: The name of the person to send the message to
    @param message: The message to send
    """
    @abstractmethod
    def send_message(self, name, message):
        pass


"""
The TextMessenger class is an implementation of the abstract base class messenger to send text messages
"""


class TextMessenger(Messenger):

    """
    The constructor of the text messenger class

    @param: config: A Config object with a configuration file loaded. Expecting
    """
    def __init__(self, config: Config):
        super().__init__(config)
        self._sms_gateways = {"sprint": "pm.sprint.com",
                              "at&t": "mms.att.net",
                              "t-mobile": "tmomail.net",
                              "verizon": "vtext.com"}

    """
    The destructor of the class to call super's destructor
    """
    def __del__(self):
        super().__del__()

    """
    The send_message function sends a text message to a number in the names_to_numbers config array
    
    @param: name: The name of the person to send the message to
    @param: message: The message to send
    """
    def send_message(self, name, message):
        try:
            numbers_dict = self._messenger_dict["names_to_numbers"]
        except KeyError:
            self._logger.log('No names_to_numbers mapping included in the config', LogLevel.ERROR)
            return
        try:
            if self._server_connection is None:
                self._connect_server()
            else:
                m = f'From: Pi Eye {self._messenger_dict["messenger_login"]["email_address"]}\n' \
                         f'To: {name} {numbers_dict[name][0]}@{self._sms_gateways[numbers_dict[name][1].lower()]}\n' \
                         f'Subject: PiEye Message\n' \
                         f'{message}\n'
                self._server_connection.sendmail('PiEye', f'{numbers_dict[name][0]}@'
                                                          f'{self._sms_gateways[numbers_dict[name][1].lower()]}', m)
        except KeyError:
            self._logger.log(f'{name} did not exist in the names_to_numbers dict', LogLevel.ERROR)
        except Exception as e:
            self._logger.log(f'The exception {e} was triggered', LogLevel.ERROR)
        finally:
            return
