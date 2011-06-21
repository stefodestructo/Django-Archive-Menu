# archive_menu.py

__author__ = "Steffen Hunt"
__date__ = "June 2011"
__license__ = "AGPL3"
__version__ = "0.0.1"
__status__ = "Development"

from calendar import month_name

from django.conf import settings
from django.db.models import get_model
from django.template import Library, Node

register = Library()

class ArchiveMenuTemplateNode(Node):
    def __init__(self, variable_name='ArchiveMenuVar'):
        
        self.variable_name = variable_name

        # Read app settings
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
        return {self.date_field + '__year' : year}

    def get_month_filter_kargs(self, year, month):
        return dict({self.date_field + '__month' : month}.items() + 
                 self.get_year_filter_kargs(year).items())

    def get_year_list(self):
        return [datetime.year for datetime 
                in self.published_posts.dates(self.date_field, 'year', order='DESC')]

    def get_month_list(self, year):
        year_filter_kargs = self.get_year_filter_kargs(year)
        return [datetime.month for datetime in 
                    self.published_posts.filter(**year_filter_kargs).dates(
                    self.date_field, 'month', order='DESC')]


    def create_archive_menu_data(self):
        archive_menu_data = []

        # get a list of years and loop       
        for year in self.get_year_list():
            
            # create a new list that will store the current year's month data
            month_list = []

            # for every year get a list of months and loop
            for month in self.get_month_list(year):

                month_filter_kwargs = self.get_month_filter_kargs(
                                                                  year,
                                                                  month)
                
                # query the count of entries posted on the given month
                post_count = self.published_posts.filter(
                        **month_filter_kwargs).count()

                # insert a tupple consisting the current month and
                # the number of entries posted on the current month
                month_list.append((month, post_count))
            
            # insert a tuple consisting of the current year and
            # the list of month data
            archive_menu_data.append((year, month_list))
        return archive_menu_data
        
        # store the archive data into the a context variable with name given

    def render(self, context):
        context[self.variable_name] = self.create_archive_menu_data()
        
        return ''

def archive_menu(parser, token):
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

    return ArchiveMenuTemplateNode(variable_name)          


register.tag('archive_tag', archive_menu)

def int_to_month_name(month_int):
    """
    Converts the month number into the name of the month as a string.
    """
    return month_name[int(month_int)]

register.simple_tag(int_to_month_name)
