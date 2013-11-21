from models import *
from django.contrib import admin


class FeaturedItemAdmin(admin.ModelAdmin):
    list_display = ('name','url','feature_date')
    list_filter = ('feature_date',)
    raw_id_fields = ('image',)

class FeaturedItemImageAdmin(admin.ModelAdmin):
    list_display = ('id','admin_thumbnail')
admin.site.register(FeaturedItemImage,FeaturedItemImageAdmin)
admin.site.register(FeaturedItem, FeaturedItemAdmin)