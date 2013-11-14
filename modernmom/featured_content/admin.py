from models import *
from django.contrib import admin


class FeaturedItemAdmin(admin.ModelAdmin):
    list_display = ('name','url','feature_date')
    list_filter = ('feature_date',)
    
admin.site.register(FeaturedItemImage)
admin.site.register(FeaturedItem, FeaturedItemAdmin)