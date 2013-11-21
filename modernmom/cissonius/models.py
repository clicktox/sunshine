from django.db import models
from photologue.models import ImageModel
from tagging.fields import TagField
from fields import UUIDField

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
    
from django.core.urlresolvers import reverse
import datetime
from fields import UUIDField


class Category(models.Model):
    name = models.CharField(max_length=255)
    descirption = models.TextField()
    parent = models.ForeignKey('self',blank=True,null=True)
    
    def __unicode__(self):
        return u'%s' % self.name

class ProducerImage(ImageModel):
    title = models.CharField(max_length=255)
    source = models.URLField(max_length=500)
       
class Producer(models.Model):
    name = models.CharField(max_length=255)
    uuid = UUIDField()
    image = models.ForeignKey(ProducerImage,blank=True,null=True)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return reverse('producer_detail',args=[self.uuid])
   
    

class ProducerLink(models.Model):
    producer = models.ForeignKey(Producer)
    url = models.URLField(max_length=500)
    label = models.CharField(max_length=255)
            
class Retailer(models.Model):
    name = models.CharField(max_length=255)
    uuid = UUIDField()
    image = models.ForeignKey(ProducerImage,blank=True,null=True)
    
class ProductImage(ImageModel):
    title = models.CharField(max_length=255)
    source = models.URLField(max_length=500)
    
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    uuid = UUIDField()
    description = models.TextField(blank=True,null=True)
    image = models.ForeignKey(ProductImage,blank=True,null=True)
    producer = models.ForeignKey(Producer,blank=True,null=True)
    
    def get_absolute_url(self):
        return reverse('product_detail',args=[self.uuid])
    
    def __unicode__(self):
        return u'%s' % self.name

class ProductReview(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    review = models.TextField()
    reviewed_on = models.DateTimeField(default=datetime.datetime.today())
    public = models.BooleanField(default=False)
    score = models.IntegerField(choices=((1,'Poor'),(2,'Fair'),(3,'Good'),(4,'Great'),(5,'Amazing')))
    
    def score_to_stars(self):
       s = ''
       for r in range(1,self.score):
           s = u'%s<i class="icon-star "></i>' % s
       return s
    
class ProductCategory(models.Model):
    product = models.ForeignKey(Product)
    category = models.ForeignKey(Category)

class ProductRetailer(models.Model):
    product = models.ForeignKey(Product)
    retailer = models.ForeignKey(Retailer)

PRODUCT_LINK_CHOICES = (('primary','Primary Product Page'),('purchase','Purchase Link'),('information','More Information'))
class ProductLink(models.Model):
    product = models.ForeignKey(Product)
    url = models.URLField(max_length=500)
    label = models.CharField(max_length=255)
    link_type = models.CharField(max_length=255,choices=PRODUCT_LINK_CHOICES, default='primary')

#MUST HAVES
class ProductMustHave(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    added_on = models.DateTimeField(default=datetime.datetime.now())

#MUSTHAVE LISTS
class GroupMustHaveImage(ImageModel):
    title = models.CharField(max_length=255)

class GroupMustHave(models.Model):
    user = models.ForeignKey(User,related_name='groupmusthaves')
    uuid = UUIDField()
    title = models.CharField(max_length=255)
    image = models.ForeignKey(GroupMustHaveImage,blank=True,null=True)
    slug = models.SlugField(max_length=255,unique=True)
    description = models.TextField()
    parent = models.ForeignKey('self',blank=True,null=True)
    
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('groupmusthave_detail',args=[self.user.username,self.slug])
    
    #sometimes you need the relative ( like for Google Analytics )
    def get_relative_url(self):
        return django_reverse('musthave_detail',args=[self.slug])

class GroupMustHaveProduct(models.Model):
    groupmusthave = models.ForeignKey(GroupMustHave)
    productmusthave = models.ForeignKey(ProductMustHave)
    
    def product(self):
        return self.productmusthave.product
    
    
#GIFTGUIDES
class GiftGuideImage(ImageModel):
    title = models.CharField(max_length=255)

class GiftGuide(models.Model):
    title = models.CharField(max_length=255)
    image = models.ForeignKey(GiftGuideImage,blank=True,null=True)
    slug = models.SlugField(max_length=255,unique=True)
    description = models.TextField()
    parent = models.ForeignKey('self',blank=True,null=True)
    
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('giftguide_detail',args=[self.slug])
    
    #sometimes you need the relative ( like for Google Analytics )
    def get_relative_url(self):
        return django_reverse('giftguide_detail',args=[self.slug])

class GiftGuideTitleBanner(ImageModel):
    title = models.CharField(max_length=255)
    giftguide = models.ForeignKey(GiftGuide)
    
class GiftGuideProductImage(ImageModel):
    title = models.CharField(max_length=255)
    source = models.URLField(max_length=500)
    
class GiftGuideProduct(models.Model):
    giftguide = models.ForeignKey(GiftGuide)
    name = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    product = models.ForeignKey(Product)
    active = models.BooleanField(default=False)
    added_by = models.ForeignKey(User)
    image = models.ForeignKey(GiftGuideImage,blank=True,null=True) 
    
    def __unicode__(self):
        if (not self.name):
            return self.product.name
        return u'%s' % self.name
   
    @property
    def description(self):
        if self.description:
            return self.description
        else:
            return self.product.description
    
    def get_slideshow_url(self):
        return u'%s#%s' % (self.giftguide.get_absolute_url(),self.id )
        
    @property
    def clickthrough(self):
        try:
            return self.giftguideproductlink.link
        except:
            return self.item.source

class GiftGuideProductLink(models.Model):
    giftguideproduct = models.OneToOneField(GiftGuideProduct)
    link = models.URLField(max_length=255)

    def __unicode__(self):
        return self.link


class PromotedGiftGuideProduct(models.Model):
    giftguideproduct = models.OneToOneField(GiftGuideProduct)
    score = models.IntegerField()
    
class GiftGuideProductCost(models.Model):
    giftguideproduct = models.OneToOneField(GiftGuideProduct)
    cost = models.FloatField()
    def __unicode__(self):
        return u'$%.2f' % self.cost


class GiftGuideFilter(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)

    def __unicode__(self):
        return u'%s' % self.name

class GiftGuideProductFilter(models.Model):
    giftguideproduct = models.ForeignKey(GiftGuideProduct)
    giftguidefilter = models.ForeignKey(GiftGuideFilter)

    def __unicode__(self):
        return self.giftguidefilter.name



#COUPONS
class Coupon (models.Model):
    title = models.CharField(max_length=500)
    uuid = UUIDField()
    description = models.CharField(max_length=1500)
    tags = TagField()
    shared_at = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.title



class CouponCode(models.Model):
    coupon = models.OneToOneField(Coupon,related_name='coupon_code')
    code = models.CharField(max_length=500)
    goto = models.URLField(max_length=500,blank=True,null=True)

from manager import ActiveCouponManager,EndsTodayCouponManager
class CouponPeriod(models.Model):
    coupon = models.OneToOneField(Coupon,related_name='coupon_period')
    starts_on = models.DateTimeField(null=True,blank=True)
    ends_on = models.DateTimeField(null=True,blank=True)
    objects = models.Manager()
    active = ActiveCouponManager(from_date='starts_on', to_date='ends_on')
    endstoday = EndsTodayCouponManager(to_date='ends_on')

    class Meta:
        ordering = ['-ends_on']

class CouponRestriction(models.Model):
    coupon = models.ForeignKey(Coupon)
    restriction = models.CharField(max_length=1500)
    details = models.TextField()
    def __unciode__(self):
        return self.name
    
