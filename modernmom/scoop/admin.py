from django.contrib import admin
from scoop.models import *

class ScoopTopicTwitterInline(admin.TabularInline):
    model = ScoopTopicTwitter

class ScoopTopicAdmin(admin.ModelAdmin):
    inlines = [ScoopTopicTwitterInline,]

admin.site.register(ScoopTopicTwitter)
admin.site.register(ScoopTopic,ScoopTopicAdmin)






