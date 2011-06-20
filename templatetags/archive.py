# archive.py

from blog.models import Post

from django.template import Library
from calendar import month_name

register = Library()

def archive():
    """
    """

    archive_list = []
    temp_year_list = []
    
    all_posts = Post.objects.exclude(is_draft__exact=True).order_by('-date')

    for post in all_posts:
        year = post.date.year
        month = post.date.strftime("%m")
        if year not in temp_year_list:
            temp_month_list = [month]
            temp_year_list.append(year)
            archive_list.append([str(year), [[month, 1]]])
        else:
            if month not in temp_month_list:
                archive_list[-1][1].append([month, 1])
            else:
                archive_list[-1][1][-1][1] += 1

    
    return {'archive_list' : archive_list}

register.inclusion_tag('archive_template.html')(archive)


def int_to_month_name(month_int):
    return month_name[int(month_int)]

register.simple_tag(int_to_month_name)

