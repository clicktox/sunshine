from django.contrib import admin
from models import *


class ContestDescriptionInline(admin.TabularInline):
    model = ContestDescription

class ContestImageInline(admin.TabularInline):
    model = ContestImage
    
class ContestAdmin(admin.ModelAdmin):
    list_display = ('name','guid')
    inlines = (ContestDescriptionInline,ContestImageInline)
admin.site.register(Contest, ContestAdmin)
admin.site.register(ContestImage)
admin.site.register(Contestant)
class ContestantEntryAdmin(admin.ModelAdmin):
    list_display = ('contestant','contest')
    list_filter = ('contest',)
admin.site.register(ContestantEntry,ContestantEntryAdmin)

class ContestantEntryImageAdmin(admin.ModelAdmin):
    list_display = ('contestantentry','admin_thumbnail')

admin.site.register(ContestantEntryImage,ContestantEntryImageAdmin)


admin.site.register(ContestDescription)

class ContestantEntryKeyAdmin(admin.ModelAdmin):
    list_display = ('contestantentry','entry_key','entry_value')
    list_filter = ('entry_key',)
admin.site.register(ContestantEntryKey,ContestantEntryKeyAdmin)

class ContestShareAdmin(admin.ModelAdmin):
    list_display = ('contest','contestant','shared_on')
    list_filter = ('contest',)
admin.site.register(ContestantShare, ContestShareAdmin)
