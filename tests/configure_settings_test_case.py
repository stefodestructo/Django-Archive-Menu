"""
"""

__author__ = "Steffen Hunt"
__credits__ = ["Steffen Hunt"]
__date__ = "July 2011"
__license__ = "GPL3"
__version__ = "0.0.1"
__status__ = "Development"

from django.conf import settings
from django.test import TestCase

class ConfigureSettingsTestCase(TestCase):
    """
    """
    def setup_settings(self, query_filter=None):
        """
        """
        self.app_name_old = settings.ARCHIVE_MENU_APP
        self.model_name_old = settings.ARCHIVE_MENU_MODEL
        self.date_field_old = settings.ARCHIVE_MENU_DATE_FIELD
        self.query_filter_old = settings.ARCHIVE_MENU_QUERY_FILTER

        settings.ARCHIVE_MENU_APP = 'archive_menu'
        settings.ARCHIVE_MENU_MODEL = 'TempModel'
        settings.ARCHIVE_MENU_DATE_FIELD = 'date'
        settings.ARCHIVE_MENU_QUERY_FILTER = query_filter

    def teardown_settings(self):
        """
        """
        settings.ARCHIVE_MENU_APP = self.app_name_old
        settings.ARCHIVE_MENU_MODEL = self.model_name_old
        settings.ARCHIVE_MENU_DATE_FIELD = self.date_field_old
        settings.ARCHIVE_MENU_QUERY_FILTER = self.query_filter_old

