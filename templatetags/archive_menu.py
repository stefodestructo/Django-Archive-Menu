"""
"""
__author__ = "Steffen Hunt"
__credits__ = ["Steffen Hunt"]
__date__ = "July 2011"
__license__ = "GPL3"
__version__ = "0.0.1"
__status__ = "Development"

from calendar import month_name

from django.conf import settings
from django.db.models import get_model
from django.template import Library, Node, Variable, VariableDoesNotExist

register = Library()

class ArchiveStatistics():
    """
    """

    def __init__(self):
        """
        """
        self.app_name = settings.ARCHIVE_MENU_APP
        self.model_name = settings.ARCHIVE_MENU_MODEL
        self.date_field = settings.ARCHIVE_MENU_DATE_FIELD
        self.query_filter = settings.ARCHIVE_MENU_QUERY_FILTER

        archived_model = get_model(self.app_name, self.model_name)
        
        if self.query_filter != None:
            self.published_posts = archived_model.objects.filter(
                                                    **self.query_filter)
        else:
            self.published_posts = archived_model.objects.all()

    def get_year_filter_kargs(self, year):
        """
        """
        return {self.date_field + '__year' : year}

    def get_month_filter_kargs(self, year, month):
        """
        """
        month_filter_kargs = ''
        return dict({self.date_field + '__month' : month}.items() + 
                 self.get_year_filter_kargs(year).items())

    def get_posts_in_month(self, year, month):
        """
        """
        month_filter_kwargs = self.get_month_filter_kargs(year, month)
        return self.published_posts.filter(**month_filter_kwargs).count()


    def get_year_list(self):
        """
        """
        return [datetime.year for datetime 
                in self.published_posts.dates(self.date_field, 'year', order='DESC')]

    def get_month_list(self, year):
        """
        """
        year_filter_kargs = self.get_year_filter_kargs(year)
        return [datetime.month for datetime in 
                    self.published_posts.filter(**year_filter_kargs).dates(
                    self.date_field, 'month', order='DESC')]


class GetYearsTemplateNode(Node):
    """
    """
    def __init__(self, variable_name='ArchiveMenu'):
        """
        """
        self.variable_name = variable_name

    def render(self, context):
        context[self.variable_name] = ArchiveStatistics().get_year_list()

        return ''

def get_years(parser, token):
    # split the consisting of the contents of the called tag and
    # strip out the first word which's value is the name of the tag
    tag_parameters = token.split_contents()[1:]

    variable_name = ''
    
    # if there's two parameters store the last parameter
    # this assumes the first parameter equals 'as'
    # as of now, testing the value of the first parameter doesn't seem necessary
    if len(tag_parameters) == 2:
        variable_name = tag_parameters[1]

    # if tag was called with only one parameter, store that parameter
    elif len(tag_parameters) == 1:
        variable_name = tag_parameters[0]

    return GetYearsTemplateNode(variable_name)          

register.tag('archive_get_years', get_years)

class GetMonthsTemplateNode(Node):
    """
    """
    def __init__(self, year, variable_name='ArchiveMenu'):
        """
        """
        self.variable_name = variable_name
        self.year = Variable(year)

    def render(self, context):
        try:
            year = self.year.resolve(context)
        except VariableDoesNotExist:
            return ''

        context[self.variable_name] = ArchiveStatistics().get_month_list(year)

        return ''

def get_months(parser, token):
    # split the consisting of the contents of the called tag and
    # strip out the first word which's value is the name of the tag
    tag_parameters = token.split_contents()[1:]

    variable_name = ''

    year = tag_parameters[0]
    
    # if there's three parameters store the last parameter
    # this assumes the second parameter equals 'as'
    # testing the value of the second parameter doesn't seem necessary

    if len(tag_parameters) == 3:
        variable_name = tag_parameters[2]

    # if tag was called with only one parameter, store that parameter
    elif len(tag_parameters) == 2:
        variable_name = tag_parameters[1]

    return GetMonthsTemplateNode(year, variable_name)          

register.tag('archive_get_months', get_months)

class CountPostsInMonthTemplateNode(Node):
    """
    """
    def __init__(self, year, month, variable_name='PostsInMonth'):
        """
        """
        self.variable_name = variable_name
        self.year = Variable(year)
        self.month = Variable(month)

    def render(self, context):
        try:
            year = self.year.resolve(context)
            month = self.month.resolve(context)
        except VariableDoesNotExist:
            return ''

        context[self.variable_name] = ArchiveStatistics().get_posts_in_month(year, month)

        return ''

def count_posts_in_month(parser, token):
    # split the consisting of the contents of the called tag and
    # strip out the first word which's value is the name of the tag
    tag_parameters = token.split_contents()[1:]

    variable_name = ''

    year = tag_parameters[0]
    month = tag_parameters[1]
    
    # if there's four parameters store the last parameter
    # this assumes the second parameter equals 'as'

    if len(tag_parameters) == 4:
        variable_name = tag_parameters[3]

    elif len(tag_parameters) == 3:
        variable_name = tag_parameters[2]

    return CountPostsInMonthTemplateNode(year, month, variable_name)          

register.tag('archive_count_posts_in_month', count_posts_in_month)

def int_to_month_name(month_int):
    """
    Converts the month number into the name of the month as a string.
    """
    return month_name[int(month_int)]

register.simple_tag(int_to_month_name)
