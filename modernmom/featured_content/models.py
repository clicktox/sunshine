from django.db import models
from fields import UUIDField
from photologue.models import ImageModel

# Create your models here.
class FeaturedItemImage(ImageModel):
    uuid = UUIDField()
    caption = models.CharField(max_length=255,blank=True,null=True)
    source = models.CharField(max_length=255,blank=True,null=True)
    
class FeaturedItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    caption = models.CharField(max_length=2500,blank=True,null=True)
    image = models.ForeignKey(FeaturedItemImage)
    url = models.URLField()
    feature_date = models.DateField()
    priority = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-feature_date','-priority')

    def get_absolute_url(self):
        return self.url
    
    def __unicode__(self):
        return u'%s' % self.name

