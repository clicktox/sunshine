from django.db import models
from tagging.fields import TagField
from photologue.models import ImageModel
from fields import UUIDField
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


try:
    __import__('subdomains')
    from subdomains.utils import reverse as _reverse
except ImportError:
    from django.core.urlresolvers import reverse as _reverse
#by doing this, we can still preserve the code struction ( reverse ) but override with desired subdomain...
def reverse(viewname, subdomain=None, scheme=None, args=None, kwargs=None,current_app=None):
    return _reverse(viewname, subdomain=None, scheme=scheme, args=args, kwargs=kwargs,current_app=current_app)


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    uuid = UUIDField()
    parent = models.ForeignKey('self',blank=True,null=True,related_name="children")
    priority = models.IntegerField(default=0)
    tags = TagField(max_length=2500)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        if not self.parent:
            return reverse('category_detail',args=[self.slug])
        else:
            return reverse('subcategory_detail',args=[self.parent.slug,self.slug])

class CategoryImage(ImageModel):
    category = models.OneToOneField(Category)

class CategoryItem(models.Model):
    """
    Holds the relationship between a tag and the item being tagged.
    """
    category = models.ForeignKey(Category, verbose_name=_('category'), related_name='items')
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id    = models.PositiveIntegerField(_('object id'), db_index=True)
    object       = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        # Enforce unique tag association per object
        unique_together = (('category', 'content_type', 'object_id'),)
        verbose_name = _('category item')
        verbose_name_plural = _('category items')

    def __unicode__(self):
        return u'%s' % (self.object)
    

class Topic(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    uuid = UUIDField()
    parent = models.ForeignKey('self',blank=True,null=True)
    priority = models.IntegerField(default=0)
    tags = TagField(max_length=2500)

    def __unicode__(self):
        return u'%s' % self.name
    
class Scoop(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    uuid = UUIDField()
    parent = models.ForeignKey('self',blank=True,null=True)
    priority = models.IntegerField(default=0)
    tags = TagField(max_length=2500)

    def __unicode__(self):
        return u'%s' % self.name

class ScoopItem(models.Model):
    """
    Holds the relationship between a tag and the item being tagged.
    """
    scoop = models.ForeignKey(Scoop, verbose_name=_('scoop'), related_name='items')
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id    = models.PositiveIntegerField(_('object id'), db_index=True)
    object       = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        # Enforce unique tag association per object
        unique_together = (('scoop', 'content_type', 'object_id'),)
        verbose_name = _('scoop item')
        verbose_name_plural = _('scoop items')

    def __unicode__(self):
        return u'%s' % (self.object)
