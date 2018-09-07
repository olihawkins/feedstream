# -*- coding: utf-8 -*-

# Imports ---------------------------------------------------------------------

import json
import os
import sys

# Constants -------------------------------------------------------------------

DIR_APP = 'app'
DIR_DATA = 'data'
DIR_TEMPLATE = 'templates'
DIR_CONFIG = 'config'
DIR_TIMESTAMP = 'timestamp'
DIR_RECIPIENT = 'recipients'

FILE_CONFIG = 'config.json'
FILE_TIMESTAMP = 'timestamp.txt'
FILE_RECIPIENT = 'recipients.json'

KEY_TIMEZONE = 'timezone'
KEY_ENTERPRISE = 'enterprise'
KEY_DOWNLOAD_NEW = 'download_new'
KEY_DOWNLOAD_PREFIX = 'download_prefix'
KEY_ACCESS_TOKEN = 'access_token'
KEY_REFRESH_TOKEN = 'refresh_token'
KEY_MAILER_ENDPOINT = 'mailer_endpoint'

# Exceptions ------------------------------------------------------------------

class Error(Exception):

    """Base class for exceptions in this module."""
    pass


class ConfigurationError(Error):

    """ Exception raised for configuration errors."""

    def __init__(self, msg):
        self.msg = msg

# Settings class --------------------------------------------------------------

class Settings:

    def __init__(self, app_dir):

        """Inititalise the settings from the config file."""

        self.app_dir = app_dir
        self.data_dir = os.path.join(self.app_dir, DIR_DATA)
        self.template_dir = os.path.join(self.app_dir, DIR_TEMPLATE)
        self.config_dir = os.path.join(self.app_dir, DIR_CONFIG)
        self.timestamp_dir = os.path.join(self.app_dir, DIR_TIMESTAMP)
        self.recipient_dir = os.path.join(self.app_dir, DIR_RECIPIENT)
        self.config_file = os.path.join(self.config_dir, FILE_CONFIG)
        self.timestamp_file = os.path.join(self.timestamp_dir, FILE_TIMESTAMP)
        self.recipient_file = os.path.join(self.recipient_dir, FILE_RECIPIENT)

        try:
            conf = json.loads(open(self.config_file).read())

            if KEY_TIMEZONE in conf and conf[KEY_TIMEZONE] != '':
                self.timezone = conf[KEY_TIMEZONE]
            else:
                raise ConfigurationError(
                    'No timezone key defined in {0}'.format(
                        self.config_file))

            if KEY_ENTERPRISE in conf and conf[KEY_ENTERPRISE] != '':
                self.enterprise = conf[KEY_ENTERPRISE]
            else:
                raise ConfigurationError(
                    'No enterprise key defined in {0}'.format(
                        self.config_file))

            if KEY_DOWNLOAD_NEW in conf and conf[KEY_DOWNLOAD_NEW] != '':
                self.download_new = conf[KEY_DOWNLOAD_NEW]
            else:
                raise ConfigurationError(
                    'No download_new key defined in {0}'.format(
                        self.config_file))

            if KEY_DOWNLOAD_PREFIX in conf and conf[KEY_DOWNLOAD_PREFIX] != '':
                self.download_prefix = conf[KEY_DOWNLOAD_PREFIX]
            else:
                raise ConfigurationError(
                    'No download_prefix key defined in {0}'.format(
                        self.config_file))

            if KEY_ACCESS_TOKEN in conf and conf[KEY_ACCESS_TOKEN] != '':
                self.access_token = conf[KEY_ACCESS_TOKEN]
            else:
                raise ConfigurationError(
                    'No access_token key defined in {0}'.format(
                        self.config_file))

            if self.enterprise:
                if KEY_REFRESH_TOKEN in conf and conf[KEY_REFRESH_TOKEN] != '':
                    self.refresh_token = conf[KEY_REFRESH_TOKEN]
                else:
                    raise ConfigurationError(
                        'No referesh_token key defined in {0}'.format(
                            self.config_file))

            if KEY_MAILER_ENDPOINT in conf and conf[KEY_MAILER_ENDPOINT] != '':
                self.mailer_endpoint = conf[KEY_MAILER_ENDPOINT]
            else:
                raise ConfigurationError(
                    'No mailer_endpoint key defined in {0}'.format(
                        self.config_file))

        except FileNotFoundError as e:
            raise ConfigurationError(
                'Could not find the configuration file: {0}'.format(
                    self.config_file))

        except json.JSONDecodeError as e:
            raise ConfigurationError(
                'Could not parse the configuration file: {0} \n{1}'.format(
                    self.config_file, e.msg))

    def save(self):

        """Save the settings to the config file."""

        conf = {}
        conf[KEY_TIMEZONE] = self.timezone
        conf[KEY_ENTERPRISE] = self.enterprise
        conf[KEY_DOWNLOAD_NEW] = self.download_new
        conf[KEY_DOWNLOAD_PREFIX] = self.download_prefix
        conf[KEY_ACCESS_TOKEN] = self.access_token
        conf[KEY_REFRESH_TOKEN] = self.refresh_token
        conf[KEY_MAILER_ENDPOINT] = self.mailer_endpoint

        with open(self.config_file, 'w') as f:
            f.write(json.dumps(conf, indent=0, sort_keys=False))


# Inititalise settings --------------------------------------------------------

try:
    settings = Settings(DIR_APP)
except ConfigurationError as e:
    sys.exit('Configuration error: {0}'.format(e.msg))
