from django.utils.safestring import mark_safe
from taxonomy.models import Category
from featured_content.models import FeaturedItem
from contests.models import Contest
from articles.models import Author
import datetime

def taxonomy(request):
    context = {}
    context['CHANNELS'] = Category.objects.all() 
    context['TOP_LEVEL_CATEOGORIES'] = Category.objects.filter(parent=None) 
    

    return context

def featured(request):
    context = {}
    context['FEATURED_ITEMS'] = FeaturedItem.objects.filter(feature_date=datetime.date.today())
    context['ACTIVE_CONTEST_LIST'] = Contest.objects.all() #.filter(feature_date=datetime.date.today())
    context['FEATURED_AUTHOR_LIST'] = Author.objects.exclude(featuredauthor=None).order_by('-featuredauthor__priority') #.filter(feature_date=datetime.date.today())
    

    return context

from django.contrib.sites.models import Site

def site_processor(request):
    return { 'SITE_BASEURL': Site.objects.get_current().domain, 'SITE_DISPLAY': Site.objects.get_current().name}