from django.utils.safestring import mark_safe
from jumplinks.models import *
from photologue.models import PhotoSize,PhotoSizeCache
import datetime

def jumplinks(request):
    context = {}
    #lets make sure we have the right size...
    photosize = PhotoSizeCache().sizes.get('300X120')
    context['jumplinks_300X120'] = Link.objects.filter(linkimage__size=photosize).order_by('?')[0]
    

    return context
