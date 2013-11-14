from django.db import models
from photologue.models import PhotoSize,ImageModel,PhotoSizeCache
from fields import UUIDField
import datetime
# Create your models here.

class Link(models.Model):
    uuid=UUIDField(max_length=36)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=1500)
    active_on = models.DateTimeField(default=datetime.datetime.now())
    active_until = models.DateTimeField(blank=True,null=True)
    priority = models.IntegerField(default=0,choices=((0,"Low"),(50,'Medium'),(100,'High')))
    
    def get_300x120_url(self):
        try:
            photosize = PhotoSizeCache().sizes.get('300X120')
            return self.linkimage_set.get(size=photosize).get_300X120_url()
        except:
            return 'no'
    
    def get_tracking_onclick(self):
        code = u"trackOutboundLink(this, 'Jump Links', '%s'); return false;" % self.url
        return code
        #return u'<a href="%s" onClick="%s">' % (self.url,code)
    
class LinkImage(ImageModel):
    size = models.ForeignKey(PhotoSize)
    link = models.ForeignKey(Link)
    
    class Meta:
        unique_together = ('size','link')
    