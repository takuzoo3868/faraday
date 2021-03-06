from __future__ import absolute_import
# Faraday Penetration Test IDE
# Copyright (C) 2016  Infobyte LLC (http://www.infobytesec.com/)
# See the file 'doc/LICENSE' for the license information

import os
import shutil
import errno
import ConfigParser

from logging import (
    DEBUG,
    INFO,
)
from config import globals as CONSTANTS
from config.configuration import getInstanceConfiguration

LOGGING_LEVEL = INFO

FARADAY_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FARADAY_SERVER_SESSIONS_DIR = os.path.join(CONSTANTS.CONST_FARADAY_HOME_PATH, 'session')
if not os.path.exists(CONSTANTS.CONST_FARADAY_HOME_PATH):
    os.mkdir(CONSTANTS.CONST_FARADAY_HOME_PATH)
if not os.path.exists(FARADAY_SERVER_SESSIONS_DIR):
    # Temporary hack, remove me
    os.mkdir(FARADAY_SERVER_SESSIONS_DIR)
FARADAY_SERVER_PID_FILE = os.path.join(
    CONSTANTS.CONST_FARADAY_HOME_PATH, 'faraday-server-port-{0}.pid')
REQUIREMENTS_FILE = os.path.join(FARADAY_BASE, 'requirements_server.txt')
DEFAULT_CONFIG_FILE = os.path.join(FARADAY_BASE, 'server/default.ini')
VERSION_FILE = os.path.join(FARADAY_BASE, CONSTANTS.CONST_VERSION_FILE)
REPORTS_VIEWS_DIR = os.path.join(FARADAY_BASE, 'views/reports')
LOCAL_CONFIG_FILE = os.path.expanduser(
    os.path.join(CONSTANTS.CONST_FARADAY_HOME_PATH, 'config/server.ini'))
LOCAL_REPORTS_FOLDER = os.path.expanduser(
    os.path.join(CONSTANTS.CONST_FARADAY_HOME_PATH, 'uploaded_reports/'))

CONFIG_FILES = [DEFAULT_CONFIG_FILE, LOCAL_CONFIG_FILE]
WS_BLACKLIST = CONSTANTS.CONST_BLACKDBS

if not os.path.exists(LOCAL_REPORTS_FOLDER):
    try:
        os.makedirs(LOCAL_REPORTS_FOLDER)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise



def copy_default_config_to_local():

    if os.path.exists(LOCAL_CONFIG_FILE):
        return

    # Create directory if it doesn't exist
    try:
        os.makedirs(os.path.dirname(LOCAL_CONFIG_FILE))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Copy default config file into faraday local config
    shutil.copyfile(DEFAULT_CONFIG_FILE, LOCAL_CONFIG_FILE)

    from server.utils.logger import get_logger
    get_logger(__name__).info(u"Local faraday-server configuration created at {}".format(LOCAL_CONFIG_FILE))


def parse_and_bind_configuration():
    """Load configuration from files declared in this module and put them
    on this module's namespace for convenient access"""

    __parser = ConfigParser.SafeConfigParser()
    __parser.read(CONFIG_FILES)

    class ConfigSection(object):
        def __init__(self, name, parser):
            self.__name = name
            self.__parser = parser

        def __getattr__(self, option_name):
            return self.__parser.get(self.__name, option_name)

    for section in __parser.sections():
        globals()[section] = ConfigSection(section, __parser)


def __get_version():
    try:
        version = open(VERSION_FILE, 'r').read().strip()
    except:
        version = ''
    return version


def __get_osint():
    try:
        return getInstanceConfiguration().getOsint()
    except:
        return ''


def gen_web_config():
    # Warning: This is publicly accesible via the API, it doesn't even need an
    # authenticated user. Don't add sensitive information here.
    doc = {
        'ver': __get_version(),
        'lic_db': CONSTANTS.CONST_LICENSES_DB,
        "osint": __get_osint(),
        'vuln_model_db': CONSTANTS.CONST_VULN_MODEL_DB
    }
    return doc


def is_debug_mode():
    return LOGGING_LEVEL is DEBUG


parse_and_bind_configuration()
