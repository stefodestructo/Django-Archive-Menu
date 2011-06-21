# archive_menu.py

__author__ = "Steffen Hunt"
__date__ = "June 2011"
__license__ = "AGPL3"
__version__ = "0.0.1"
__status__ = "Development"

# TODO - Add module metadata
# TODO - Write docstrings for all test modules, classes and methods
# TODO - Refactor code to make it easier to test
# TODO - Create a git repo for the app
# TODO - Post app on github.com
# TODO - install archive_menu app onto the yakko blog
# TODO - run tests on yakko
# TODO - remove old archive_menu code from the yakko blog



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

    def create_archive_menu_data(self):
        archive_menu_data = []

        archived_model = get_model(self.app_name, self.model_name)
        
        if self.query_filter != None:
            published_posts = archived_model.objects.filter(**self.query_filter)
        else:
            published_posts = archived_model.objects.all()

        # get a list of years and loop       
        for year in [datetime.year for datetime 
                in published_posts.dates(self.date_field, 'year', order='DESC')]:
            
            # create a new list that will store the current year's month data
            month_list = []

            year_filter_kwargs = {self.date_field + '__year' : year}
            
            # for every year get a list of months and loop
            for month in [datetime.month for datetime in 
                    published_posts.filter(**year_filter_kwargs).dates(
                        self.date_field, 'month', order='DESC')]:

                # a bit of hack, will change as soon as I find a better way
                # to save some filter arguments in a setup.py file
                month_filter_kwargs = dict(
                    {self.date_field + '__month' : month}.items() + 
                        year_filter_kwargs.items())
                
                # query the count of entries posted on the given month
                post_count = published_posts.filter(
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