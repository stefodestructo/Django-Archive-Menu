"""
"""
from archive_menu.tests.an_app.models import TempModel
from archive_menu.templatetags import archive_menu

from django.template import Context, Template
from django.test import TestCase

__author__ = "Steffen Hunt"
__credits__ = ["Steffen Hunt"]
__date__ = "June 2011"
__license__ = "AGPL3"
__version__ = "0.0.1"
__status__ = "Development"

# TODO - Write docstrings for all test modules, classes and methods
# TODO - Achieve 100% test coverage

class IntToMonthFunc(TestCase):
    def test_int_to_month_func(self):
        self.assertEqual(archive_menu.int_to_month_name(1), 'January')
        self.assertEqual(archive_menu.int_to_month_name(2), 'February')
        self.assertEqual(archive_menu.int_to_month_name(3), 'March')

class IntToMonthTemplateTagTest(TestCase):

    def test_int_to_month_template_tag(self):
        expected_value = 'January'

        context = Context({})
        template = Template("{% load archive_menu %}{% int_to_month_name 1 %}")
        rendered_string = template.render(context)

        self.assertEqual(rendered_string, expected_value)
