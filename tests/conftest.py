"""
"""

__author__ = "Steffen Hunt"
__credits__ = ["Steffen Hunt"]
__date__ = "July 2011"
__license__ = "GPL3"
__version__ = "0.0.1"
__status__ = "Development"

import os
import sys
sys.path.append('../..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
from django.core import management
from django.db import connection
from django.test.utils import setup_test_environment, teardown_test_environment

saved_INSTALLED_APPS = settings.INSTALLED_APPS

VERBOSITY = 0

old_name = ''

def pytest_configure(config):
    """This function is called before any tests are run."""
    old_name = settings.DATABASES['default']['NAME']
    settings.INSTALLED_APPS = tuple(list(saved_INSTALLED_APPS) + ['archive_menu.tests.an_app'])
    setup_test_environment()
    connection.creation.create_test_db(VERBOSITY)
    management.call_command('syncdb', verbosity=VERBOSITY, interactive=False)

def pytest_unconfigure(config):
    connection.creation.destroy_test_db(old_name, VERBOSITY)
    teardown_test_environment()
    settings.INSTALLED_APPS = saved_INSTALLED_APPS

def pytest_runtest_setup(item):
    """This function is called before every test."""
    pass

def pytest_runtest_teardown(item):
    """This function is called after every test calls their teardown function."""
    management.call_command('flush', verbosity=VERBOSITY, interactive=False)
