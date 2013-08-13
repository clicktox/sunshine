from django.db import models
from tagging.fields import TagField
from photologue.models import ImageModel
from fields import UUIDField
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.core.urlresolvers import reverse

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
    publish_date = models.DateTimeField(default=datetime.now, help_text=_('The date and time this article shall appear online.'))
   
    class Meta:
        # Enforce unique tag association per object
        unique_together = (('category', 'content_type', 'object_id'),)
        verbose_name = _('category item')
        verbose_name_plural = _('category items')
        ordering = ('-publish_date',)
        get_latest_by = 'publish_date'

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
    publish_date = models.DateTimeField(default=datetime.now, help_text=_('The date and time this article shall appear online.'))
   
    class Meta:
        # Enforce unique tag association per object
        unique_together = (('scoop', 'content_type', 'object_id'),)
        verbose_name = _('scoop item')
        verbose_name_plural = _('scoop items')
        ordering = ('-publish_date',)
        get_latest_by = 'publish_date'

    def __unicode__(self):
        return u'%s' % (self.object)
