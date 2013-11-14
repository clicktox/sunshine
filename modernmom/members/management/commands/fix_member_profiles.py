from django.core.management.base import NoArgsCommand
from optparse import make_option
from urlparse import urlparse,urljoin
from django.conf import settings
from datetime import datetime, timedelta
from time import strftime
import urllib2
import re

from django.utils.safestring import mark_safe
from members.models import Member
from django.contrib.auth.models import User

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
    )
    help = 'Update Category Article Counts'
    args = ''
    
    def handle_noargs(self, **options):
        users = User.objects.all()
        password = User.objects.make_random_password()
        for user in users:
            if not user.is_staff:
                try:
                    if not user.has_usable_password():
                        user.set_password(password)
                        user.save()
                except:
                    pass
                
           