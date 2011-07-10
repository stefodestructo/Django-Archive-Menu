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
from archive_menu.tests.models import TempModel

from django.template import Context, Template
from django.test import TestCase

from mock import Mock, patch


class ArchiveMenuSingleDataPointTest(ConfigureSettingsTestCase):
    """
    """

    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

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
        self.setup_settings({'is_draft' : False})

    def tearDown(self):
        self.teardown_settings()

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
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

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

class ArchiveGetYearsTagRenderTest(ConfigureSettingsTestCase):
    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

    def test_archive_menu_tag_render(self):

        test_data = [
            {'year' : 2012, 'month': 1, 'day' : 1},
            {'year' : 1990, 'month': 1, 'day' : 20},
            {'year' : 2010, 'month': 2, 'day' : 15},
            {'year' : 2010, 'month': 6, 'day' : 20},
            ]
        expected_value = [2012, 2010, 1990]

        context_var = 'archive_data'

        for kwargs in test_data:
            TempModel(date=datetime(**kwargs), is_draft=True).save()

        context = Context({})
        template = Template("{% load archive_menu %}{% archive_get_years as archive_data %}")
        rendered_string = template.render(context)

        self.assertEqual(context[context_var], expected_value)
