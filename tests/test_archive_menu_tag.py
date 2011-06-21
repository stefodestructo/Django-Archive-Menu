"""
"""

__author__ = "Steffen Hunt"
__credits__ = ["Steffen Hunt"]
__date__ = "June 2011"
__license__ = "AGPL3"
__version__ = "0.0.1"
__status__ = "Development"

from datetime import datetime

from archive_menu.templatetags import archive_menu
from archive_menu.tests.models import TempModel

from django.conf import settings
from django.template import Context, Template
from django.test import TestCase

from mock import Mock, patch

class ConfigureSettingsTestCase(TestCase):
    """
    """
    def setup_settings(self):
        """
        """
        self.app_name_old = settings.ARCHIVE_MENU_APP
        self.model_name_old = settings.ARCHIVE_MENU_MODEL
        self.date_field_old = settings.ARCHIVE_MENU_DATE_FIELD
        self.query_filter_old = settings.ARCHIVE_MENU_QUERY_FILTER

        settings.ARCHIVE_MENU_APP = 'archive_menu'
        settings.ARCHIVE_MENU_MODEL = 'TempModel'
        settings.ARCHIVE_MENU_DATE_FIELD = 'date'
        settings.ARCHIVE_MENU_QUERY_FILTER = None

    def teardown_settings(self):
        """
        """
        settings.ARCHIVE_MENU_APP = self.app_name_old
        settings.ARCHIVE_MENU_MODEL = self.model_name_old
        settings.ARCHIVE_MENU_DATE_FIELD = self.date_field_old
        settings.ARCHIVE_MENU_QUERY_FILTER = self.query_filter_old


class GetMonthFilterKargs(TestCase):
    """
    """
    def test_get_month_filter_kargs(self):
        """
        """
        archive_menu_node = archive_menu.ArchiveMenuTemplateNode()
        self.assertEqual(archive_menu_node.get_month_filter_kargs(1989, 1),
                         {'date__year' : 1989, 'date__month' : 1}
                        )


class GetYearFilterKargs(TestCase):
    """
    """
    def test_get_year_filter_kargs(self):
        """
        """
        archive_menu_node = archive_menu.ArchiveMenuTemplateNode()
        self.assertEqual(archive_menu_node.get_year_filter_kargs(1989),
                         {'date__year' : 1989}
                        )

#class GetYearListTest(TestCase):
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

        archive_menu_node = archive_menu.ArchiveMenuTemplateNode()

        self.assertEqual(archive_menu_node.get_year_list(),
                         expected_value)

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

        archive_menu_node = archive_menu.ArchiveMenuTemplateNode()

        self.assertEqual(archive_menu_node.get_month_list(2000),
                         expected_value)
        
class ArchiveMenuSingleDataPointTest(ConfigureSettingsTestCase):
    """
    """

    def setUp(self):
        self.app_name_old = settings.ARCHIVE_MENU_APP
        self.model_name_old = settings.ARCHIVE_MENU_MODEL
        self.date_field_old = settings.ARCHIVE_MENU_DATE_FIELD
        self.query_filter_old = settings.ARCHIVE_MENU_QUERY_FILTER

        settings.ARCHIVE_MENU_APP = 'archive_menu'
        settings.ARCHIVE_MENU_MODEL = 'TempModel'
        settings.ARCHIVE_MENU_DATE_FIELD = 'date'
        settings.ARCHIVE_MENU_QUERY_FILTER = None

    def tearDown(self):
        settings.ARCHIVE_MENU_APP = self.app_name_old
        settings.ARCHIVE_MENU_MODEL = self.model_name_old
        settings.ARCHIVE_MENU_DATE_FIELD = self.date_field_old
        settings.ARCHIVE_MENU_QUERY_FILTER = self.query_filter_old

    def test_create_new_archive_menu_data_with_single_data_point(self):
        """
        """

        dataundertest = TempModel(date=datetime(
                year=2000,
                month=1,
                day=1
                )).save()

        expected_value = [(2000, [(1, 1)])]

        archive_menu_node = archive_menu.ArchiveMenuTemplateNode()

        self.assertEqual(archive_menu_node.create_archive_menu_data(), expected_value)

class Querytest(ConfigureSettingsTestCase):
    """
    """

    draft_data = [
            {'year' : 2000, 'month': 1, 'day' : 1},
            {'year' : 2000, 'month': 1, 'day' : 20},
            {'year' : 2010, 'month': 2, 'day' : 15},
            {'year' : 2010, 'month': 2, 'day' : 20},
            ]

    posted_data = [
                   {'year' : 2001, 'month': 1, 'day' : 1},
                   {'year' : 2001, 'month': 1, 'day' : 26},
                   {'year' : 2010, 'month': 2, 'day' : 15},
                   {'year' : 2010, 'month': 6, 'day' : 20},
                  ]

    def setUp(self):
        self.app_name_old = settings.ARCHIVE_MENU_APP
        self.model_name_old = settings.ARCHIVE_MENU_MODEL
        self.date_field_old = settings.ARCHIVE_MENU_DATE_FIELD
        self.query_filter_old = settings.ARCHIVE_MENU_QUERY_FILTER

        settings.ARCHIVE_MENU_APP = 'archive_menu'
        settings.ARCHIVE_MENU_MODEL = 'TempModel'
        settings.ARCHIVE_MENU_DATE_FIELD = 'date'
        settings.ARCHIVE_MENU_QUERY_FILTER = {'is_draft' : False}

    def tearDown(self):
        settings.ARCHIVE_MENU_APP = self.app_name_old
        settings.ARCHIVE_MENU_MODEL = self.model_name_old
        settings.ARCHIVE_MENU_DATE_FIELD = self.date_field_old
        settings.ARCHIVE_MENU_QUERY_FILTER = self.query_filter_old


    def test_query_filter(self):

        expected_value = [
                (2010, [(6, 1), (2, 1)]),
                (2001, [(1, 2)]),
                ]

        for kwargs in self.draft_data:
            TempModel(date=datetime(**kwargs), is_draft=True).save()

        for kwargs in self.posted_data:
            TempModel(date=datetime(**kwargs), is_draft=False).save()

        archive_menu_node = archive_menu.ArchiveMenuTemplateNode()

        self.assertEqual(archive_menu_node.create_archive_menu_data(), expected_value)


class ArchiveMenuFunctionTest(TestCase):
    @patch('archive_menu.templatetags.archive_menu.ArchiveMenuTemplateNode')
    def test_archive_menu(self, mock_archive_menu_template_node):
        # create mock objects
        parser = Mock()
        token = Mock()

        token.split_contents.return_value = ('archive_tag', 'as', 'archive_data')
        
        # call function under test
        archive_menu.archive_menu(parser, token)

        # assertions
        mock_archive_menu_template_node.assert_called_with('archive_data')
        
class ArchiveMenuTagRenderTest(ConfigureSettingsTestCase):
    def setUp(self):
        self.app_name_old = settings.ARCHIVE_MENU_APP
        self.model_name_old = settings.ARCHIVE_MENU_MODEL
        self.date_field_old = settings.ARCHIVE_MENU_DATE_FIELD
        self.query_filter_old = settings.ARCHIVE_MENU_QUERY_FILTER

        settings.ARCHIVE_MENU_APP = 'archive_menu'
        settings.ARCHIVE_MENU_MODEL = 'TempModel'
        settings.ARCHIVE_MENU_DATE_FIELD = 'date'
        settings.ARCHIVE_MENU_QUERY_FILTER = None

    def tearDown(self):
        settings.ARCHIVE_MENU_APP = self.app_name_old
        settings.ARCHIVE_MENU_MODEL = self.model_name_old
        settings.ARCHIVE_MENU_DATE_FIELD = self.date_field_old
        settings.ARCHIVE_MENU_QUERY_FILTER = self.query_filter_old

    def test_archive_menu_tag_render(self):
        expected_value = [(2000, [(1, 1)])]
        context_var = 'archive_data'

        TempModel(date=datetime(
                year=2000,
                month=1,
                day=1
                )).save()

        context = Context({})
        template = Template("{% load archive_menu %}{% archive_tag as archive_data %}")
        rendered_string = template.render(context)

        self.assertEqual(context[context_var], expected_value)
