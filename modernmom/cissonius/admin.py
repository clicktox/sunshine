from django.contrib import admin
from models import *

class ProductCostInline(admin.TabularInline):
    model = ProductCost
class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 3
    
class ProductRetailerInline(admin.TabularInline):
    model = ProductRetailer
    extra = 3

class ProductLinkInline(admin.TabularInline):
    model = ProductLink
    extra = 1
    
    
class GiftGuideProductInline(admin.TabularInline):
    model = GiftGuideProduct
    exclude = ('added_by',)
    extra = 3
admin.site.register(GiftGuideTitleBanner)

class GiftGuideTitleBannerInline(admin.TabularInline):
    model = GiftGuideTitleBanner
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductCostInline,ProductLinkInline) #ProductCategoryInline,ProductRetailerInline)
    list_display = ('id','name','producer','image')
    search_fields = ('name',)
    raw_id_fields = ('image',)



admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCost)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(ProductRetailer)

class ProducerLinkInline(admin.TabularInline):
    model=ProducerLink
    extra=2
    
class ProducerAdmin(admin.ModelAdmin):
    inlines = [ProducerLinkInline,]
admin.site.register(Producer,ProducerAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id','admin_thumbnail')
admin.site.register(ProductImage,ProductImageAdmin)

class GiftGuideAdmin(admin.ModelAdmin):
    inlines = [GiftGuideTitleBannerInline,GiftGuideProductInline]
    prepopulated_fields = {'slug':('title',),}
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, GiftGuideProduct): #Check if it is the correct type of inline
                instance.added_by = request.user
                instance.save()
    
admin.site.register(GiftGuide,GiftGuideAdmin)
admin.site.register(GiftGuideImage)


class GiftGuideProductFilterInline(admin.TabularInline):
    model=GiftGuideProductFilter
    extra=2

class PromotedGiftGuideProductInline(admin.TabularInline):
    model = PromotedGiftGuideProduct
    
class GiftGuideProductAdmin(admin.ModelAdmin):
    inlines = [GiftGuideProductFilterInline,PromotedGiftGuideProductInline]
    raw_id_fields = ('product',)
    exclude = ('added_by',)
    list_display = ('product','giftguide')
    list_filter = ('giftguide',)
    
    fieldsets = (
        (None, {
            'fields': ('giftguide', 'product','active' )
        }),
        ('Overrides', {
            'fields': ('name', 'image',)
        }),
        
                 )
                 
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()
        
admin.site.register(GiftGuideProduct,GiftGuideProductAdmin)

class ProductMustHaveAdmin(admin.ModelAdmin):
    readonly_fields = ('user','product')
    list_display = ('user','product','added_on')

admin.site.register(ProductMustHave,ProductMustHaveAdmin)
admin.site.register(PromotedGiftGuideProduct)

class GroupMustHaveAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',),}
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        
admin.site.register(GroupMustHaveImage)
admin.site.register(GroupMustHave,GroupMustHaveAdmin)
admin.site.register(GroupMustHaveProduct)
admin.site.register(GiftGuideProductFilter)

class GiftGuideFilterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}
    
admin.site.register(GiftGuideFilter,GiftGuideFilterAdmin)
