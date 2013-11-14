import logging

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from models import *

class LinkImageInline(admin.TabularInline):
    model = LinkImage

class LinkAdmin(admin.ModelAdmin):
    inlines = [LinkImageInline,]
    list_display = ('url','title')
admin.site.register(Link,LinkAdmin)
admin.site.register(LinkImage)
