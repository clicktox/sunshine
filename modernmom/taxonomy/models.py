from django.db import models
from tagging.fields import TagField
from photologue.models import ImageModel
from fields import UUIDField
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.core.urlresolvers import reverse
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
    
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
    
    def get_absolute_url(self):
        return reverse('topic_detail',args=[self.uuid])

class TopicImage(ImageModel):
    topic = models.OneToOneField(Topic)
    




class TopicItem(models.Model):
    topic = models.ForeignKey(Topic, related_name='items')
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id    = models.PositiveIntegerField(_('object id'), db_index=True)
    object       = generic.GenericForeignKey('content_type', 'object_id')
    publish_date = models.DateTimeField(default=datetime.now, help_text=_('The date and time this article shall appear online.'))
   
    class Meta:
        # Enforce unique tag association per object
        unique_together = (('topic', 'content_type', 'object_id'),)
        ordering = ('-publish_date',)
        get_latest_by = 'publish_date'

    def __unicode__(self):
        return u'%s' % (self.object)
    
class TopicParticipant(models.Model):
    participant = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)
    status = models.IntegerField(default=0)
    class Meta:
        # Enforce unique tag association per object
        unique_together = (('participant', 'topic'),)
    
    def __unicode__(self):
        return self.participant.username
 
class TopicParticipantItem(models.Model):
    topicparticipant = models.ForeignKey(TopicParticipant)
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id    = models.PositiveIntegerField(_('object id'), db_index=True)
    object       = generic.GenericForeignKey('content_type', 'object_id')
    publish_date = models.DateTimeField(default=datetime.now, help_text=_('The date and time this article shall appear online.'))
   
    class Meta:
        # Enforce unique tag association per object
        unique_together = (('topicparticipant', 'content_type', 'object_id'),)
        ordering = ('-publish_date',)
        get_latest_by = 'publish_date'

    def __unicode__(self):
        return u'%s' % (self.object)
    
class Scoop(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    uuid = UUIDField()
    parent = models.ForeignKey('self',blank=True,null=True)
    priority = models.IntegerField(default=0)
    tags = TagField(max_length=2500)

    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return reverse('scoop_detail',args=[self.slug])

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
    
MARKUP_HTML = 'h'
MARKUP_MARKDOWN = 'm'
MARKUP_REST = 'r'
MARKUP_TEXTILE = 't'
MARKUP_OPTIONS = getattr(settings, 'ARTICLE_MARKUP_OPTIONS', (
        (MARKUP_HTML, _('HTML/Plain Text')),
        (MARKUP_MARKDOWN, _('Markdown')),
        (MARKUP_REST, _('ReStructured Text')),
        (MARKUP_TEXTILE, _('Textile'))
    ))
MARKUP_DEFAULT = getattr(settings, 'ARTICLE_MARKUP_DEFAULT', MARKUP_HTML)

MARKUP_HELP = _("""Select the type of markup you are using in this article.
<ul>
<li><a href="http://daringfireball.net/projects/markdown/basics" target="_blank">Markdown Guide</a></li>
<li><a href="http://docutils.sourceforge.net/docs/user/rst/quickref.html" target="_blank">ReStructured Text Guide</a></li>
<li><a href="http://thresholdstate.com/articles/4312/the-textile-reference-manual" target="_blank">Textile Guide</a></li>
</ul>""")


class TopicContent(models.Model):
    topic = models.OneToOneField(Topic)
    markup = models.CharField(max_length=1, choices=MARKUP_OPTIONS, default=MARKUP_DEFAULT, help_text=MARKUP_HELP)
    content = models.TextField()
    rendered_content = models.TextField()
    
    def save(self, *args, **kwargs):
        """Renders the article using the appropriate markup language."""
        self.do_render_markup()
        super(TopicContent, self).save(*args, **kwargs)
    
    def do_render_markup(self):
        """Turns any markup into HTML"""
        original = self.rendered_content
        if self.markup == MARKUP_MARKDOWN:
            self.rendered_content = markup.markdown(self.content)
        elif self.markup == MARKUP_REST:
            self.rendered_content = markup.restructuredtext(self.content)
        elif self.markup == MARKUP_TEXTILE:
            self.rendered_content = markup.textile(self.content)
        else:
            self.rendered_content = self.content
        return (self.rendered_content != original)
