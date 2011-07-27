"""
"""
__author__ = "Steffen Hunt"
__credits__ = ["Steffen Hunt"]
__date__ = "July 2011"
__license__ = "AGPL3"
__version__ = "0.0.1"
__status__ = "Development"

from configure_settings_test_case import ConfigureSettingsTestCase

from datetime import datetime

from archive_menu.templatetags import archive_menu
from archive_menu.tests.an_app.models import TempModel

from django.test import TestCase

class GetMonthFilterKargs(TestCase):
    """
    """
    def test_get_month_filter_kargs(self):
        """
        """
        archive_stats = archive_menu.ArchiveStatistics()
        archive_stats.date_field = 'date'
        self.assertEqual(archive_stats.get_month_filter_kargs(1989, 1),
                         {'date__year' : 1989, 'date__month' : 1}
                        )

class GetYearFilterKargs(TestCase):
    """
    """
    def test_get_year_filter_kargs(self):
        """
        """
        archive_stats = archive_menu.ArchiveStatistics()
        archive_stats.date_field = 'date'
        self.assertEqual(archive_stats.get_year_filter_kargs(1989),
                         {'date__year' : 1989}
                        )

class GetYearListTest(ConfigureSettingsTestCase):
    """
    """

    test_data = [
            {'year' : 2012, 'month': 1, 'day' : 1},
            {'year' : 1990, 'month': 1, 'day' : 20},
            {'year' : 2010, 'month': 2, 'day' : 15},
            {'year' : 2010, 'month': 6, 'day' : 20},
            ]

    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

    def test_get_year_list(self):
        """
        """
        expected_value = [2012, 2010, 1990]

        for kwargs in self.test_data:
            TempModel(date=datetime(**kwargs), is_draft=True).save()

        archive_stats = archive_menu.ArchiveStatistics()

        self.assertEqual(archive_stats.get_year_list(),
                         expected_value)

class PostInMonthTest(ConfigureSettingsTestCase):
    """
    """

    test_data = [
            {'year' : 2000, 'month': 1, 'day' : 1},
            {'year' : 2000, 'month': 1, 'day' : 20},
            {'year' : 2000, 'month': 2, 'day' : 15},
            {'year' : 2000, 'month': 6, 'day' : 20},
            ]

    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

    def test_get_month_list(self):
        """
        """

        for kwargs in self.test_data:
            TempModel(date=datetime(**kwargs), is_draft=True).save()

        archive_stats = archive_menu.ArchiveStatistics()

        
        self.assertEqual(archive_stats.get_posts_in_month(2000, 1), 2)

        self.assertEqual(archive_stats.get_posts_in_month(2000, 2), 1)

        self.assertEqual(archive_stats.get_posts_in_month(2000, 6), 1)

class GetMonthListTest(ConfigureSettingsTestCase):
    """
    """

    test_data = [
            {'year' : 2000, 'month': 1, 'day' : 1},
            {'year' : 2000, 'month': 1, 'day' : 20},
            {'year' : 2000, 'month': 2, 'day' : 15},
            {'year' : 2000, 'month': 6, 'day' : 20},
            ]

    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

    def test_get_month_list(self):
        """
        """
        expected_value = [6, 2, 1]

        for kwargs in self.test_data:
            TempModel(date=datetime(**kwargs), is_draft=True).save()

        archive_stats = archive_menu.ArchiveStatistics()

        self.assertEqual(archive_stats.get_month_list(2000),
                         expected_value)
