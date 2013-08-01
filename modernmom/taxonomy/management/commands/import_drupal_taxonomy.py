from django.core.management.base import NoArgsCommand
from optparse import make_option
from urlparse import urlparse,urljoin
from django.conf import settings
from datetime import datetime, timedelta
from time import strftime
import urllib2
import re

from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from taxonomy .models import *
from django.forms import EmailField
import MySQLdb

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
    )
    help = 'Update Category Article Counts'
    args = ''

    def handle_noargs(self, **options):
        
        sql = "SELECT name, description, weight,taxonomy_menu.tid,parent, dst FROM taxonomy_menu \
            inner join pressflow.term_hierarchy on term_hierarchy.tid = taxonomy_menu.tid \
            INNER JOIN term_data on term_data.tid = term_hierarchy.tid \
            inner join url_alias on src = concat('taxonomy/term/',term_hierarchy.tid);"

        db = MySQLdb.connect(host="localhost", user="root", passwd="r00t!", db="pressflow") # name of the data base
        cur = db.cursor()
        cur.execute(sql)
        fo_errors = open('import_taxonomy_errors','w')
        for row in cur.fetchall() :
   
            name = row[0]
            description = row[1]
            weight = int(row[2])
            tid = int(row[3])
            try:
                parent = Category.objects.get(id=int(row[4]))
            except Category.DoesNotExist:
                parent = None
            slug = row[5]
            slug = slug.split('/')[-1]
          

            try:
                try:
                    category = Category.objects.get(id=tid)
                except:
                    category = Category(id=tid,name=name,slug=slug,parent=parent,priority=weight)
                category.id = tid
                category.save()
                print u' %d vs %d' % (category.id,tid)
                    
                
            except Exception as e:
                print e
                