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

class ArchiveGetYearsTagRenderTest(ConfigureSettingsTestCase):
    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

    def test_archive_get_years_tag_render(self):

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

class ArchiveGetMonthsTagRenderTest(ConfigureSettingsTestCase):
    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

    def test_archive_get_months_tag_render(self):

        test_data = [
            {'year' : 2012, 'month': 1, 'day' : 1},
            {'year' : 1990, 'month': 1, 'day' : 20},
            {'year' : 2010, 'month': 2, 'day' : 15},
            {'year' : 2010, 'month': 6, 'day' : 20},
            ]
        expected_value = [6, 2]

        context_var = 'archive_data'

        for kwargs in test_data:
            TempModel(date=datetime(**kwargs), is_draft=True).save()

        context = Context({})
        template = Template("{% load archive_menu %}{% archive_get_months 2010 as archive_data %}")
        rendered_string = template.render(context)

        self.assertEqual(context[context_var], expected_value)

class ArchiveGetMonthsTagRenderTestUsingContextVariable(ConfigureSettingsTestCase):
    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

    def test_archive_get_months_tag_render(self):

        test_data = [
            {'year' : 2012, 'month': 1, 'day' : 1},
            {'year' : 1990, 'month': 1, 'day' : 20},
            {'year' : 2010, 'month': 2, 'day' : 15},
            {'year' : 2010, 'month': 6, 'day' : 20},
            ]
        expected_value = [6, 2]

        context_var = 'archive_data'

        for kwargs in test_data:
            TempModel(date=datetime(**kwargs), is_draft=True).save()

        context = Context({})
        context['year'] = 2010
        template = Template("{% load archive_menu %}{% archive_get_months year as archive_data %}")
        rendered_string = template.render(context)

        self.assertEqual(context[context_var], expected_value)

class ArchiveCountPostsInMonthRenderTest(ConfigureSettingsTestCase):
    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

    def test_archive_count_posts_in_month_tag_render(self):

        test_data = [
            {'year' : 2012, 'month': 1, 'day' : 1},
            {'year' : 1990, 'month': 1, 'day' : 20},
            {'year' : 2010, 'month': 2, 'day' : 15},
            {'year' : 2010, 'month': 3, 'day' : 20},
            {'year' : 2010, 'month': 6, 'day' : 20},
            {'year' : 2010, 'month': 6, 'day' : 20},
            {'year' : 2010, 'month': 6, 'day' : 11},
            {'year' : 2010, 'month': 6, 'day' : 10},
            ]
        expected_value = 4 

        context_var = 'archive_data'

        for kwargs in test_data:
            TempModel(date=datetime(**kwargs), is_draft=True).save()

        context = Context({})
        template = Template("{% load archive_menu %}{% archive_count_posts_in_month 2010 6 as archive_data %}")
        rendered_string = template.render(context)

        self.assertEqual(context[context_var], expected_value)

class ArchiveCountPostsInMonthRenderTestUsingContextVariable(ConfigureSettingsTestCase):
    def setUp(self):
        self.setup_settings()

    def tearDown(self):
        self.teardown_settings()

    def test_archive_count_posts_in_month_tag_render_using_context_variable(self):

        test_data = [
            {'year' : 2012, 'month': 1, 'day' : 1},
            {'year' : 1990, 'month': 1, 'day' : 20},
            {'year' : 2010, 'month': 2, 'day' : 15},
            {'year' : 2010, 'month': 3, 'day' : 20},
            {'year' : 2010, 'month': 6, 'day' : 20},
            {'year' : 2010, 'month': 6, 'day' : 20},
            {'year' : 2010, 'month': 6, 'day' : 11},
            {'year' : 2010, 'month': 6, 'day' : 10},
            ]
        expected_value = 4 

        context_var = 'archive_data'

        for kwargs in test_data:
            TempModel(date=datetime(**kwargs), is_draft=True).save()

        context = Context({})
        context['year'] = 2010
        context['month_int'] = 6
        template = Template("{% load archive_menu %}{% archive_count_posts_in_month year month_int as archive_data %}")
        rendered_string = template.render(context)

        self.assertEqual(context[context_var], expected_value)
