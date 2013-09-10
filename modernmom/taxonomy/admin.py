from django.contrib import admin
from models import *


admin.site.register(Topic)
admin.site.register(TopicContent)
admin.site.register(TopicImage)
admin.site.register(Scoop)
admin.site.register(ScoopItem)

class CategoryItemAdmin(admin.ModelAdmin):
    list_display = ('object','category')
    list_filter = ('category',)
admin.site.register(CategoryItem,CategoryItemAdmin)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','parent')
    list_filter = ('parent',)
    
admin.site.register(Category, CategoryAdmin)


class CategoryImageAdmin(admin.ModelAdmin):
    list_display = ('category','admin_thumbnail')
    list_per_page = 10
    
admin.site.register(CategoryImage,CategoryImageAdmin)
