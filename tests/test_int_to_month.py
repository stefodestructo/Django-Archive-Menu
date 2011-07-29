"""
"""
from archive_menu.templatetags import archive_menu

from django.template import Context, Template

__author__ = "Steffen Hunt"
__credits__ = ["Steffen Hunt"]
__date__ = "July 2011"
__license__ = "GPL3"
__version__ = "0.0.1"
__status__ = "Development"

def test_int_to_month_func():
    """
    """
    assert archive_menu.int_to_month_name(1) == 'January'
    assert archive_menu.int_to_month_name(2) == 'February'
    assert archive_menu.int_to_month_name(3) == 'March'


def test_int_to_month_template_tag():
    """
    """
    context = Context({})
    template = Template("{% load archive_menu %}{% int_to_month_name 1 %}")

    assert template.render(context) == 'January'
