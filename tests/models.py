"""
"""

__author__ = "Steffen Hunt"
__credits__ = ["Steffen Hunt"]
__date__ = "June 2011"
__license__ = "AGPL3"
__version__ = "0.0.1"
__status__ = "Development"

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

class TempModel(models.Model):
    date = models.DateTimeField(_(u'Date'), default=datetime.now)
    is_draft = models.BooleanField(verbose_name=_(u'Draft'), default=False)

    class Meta:
        app_label = 'archive_menu'
