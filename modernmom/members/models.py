from django.db import models

from fields import UUIDField
from django.conf import settings
from django.db.models.signals import post_save

import datetime,re
from django.utils import timezone
from photologue.models import ImageModel
from django.utils.timezone import now as now

from django.core.mail import send_mail
from django.core import validators
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

class SocialProfileType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return u'%s' % self.name
    
class Avatar(ImageModel):
    uuid = UUIDField()

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager

class Member(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=50, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '[space]/@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[ \w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    uuid = UUIDField()
    avatar = models.ForeignKey(Avatar,blank=True,null=True)
    slug = models.SlugField(max_length=255,blank=True,null=True)
    birthdate = models.DateTimeField(blank=True,null=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        #abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
   
    def get_absolute_url(self):
        return reverse('member_detail',args=[self.uuid])
    
class MemberVerified(models.Model):
    member = models.OneToOneField(Member,related_name='is_verified')
    verified_at = models.DateTimeField()
   
class MemberSignature(models.Model):
    member = models.OneToOneField(Member)
    signature = models.TextField()

    def __unicode__(self):
        return u'%s' % self.signature

class MemberSocialProfile(models.Model):
    member = models.ForeignKey(Member)
    profile_type = models.ForeignKey(SocialProfileType)
    url = models.URLField(max_length=255,unique=True)

class MemberWebsite(models.Model):
    member = models.ForeignKey(Member)
    website = models.URLField(max_length=500)
    description = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return u'%s' % self.website
       
    
class MemberAboutMe(models.Model):
    member = models.OneToOneField(Member)
    content = models.TextField()
    
    def __unicode__(self):
        return u'%s' % self.content

class MemberAddress(models.Model):
    member = models.OneToOneField(Member)
    street = models.CharField(max_length=255)
    additional = models.CharField(max_length=255,blank=True,null=True) 
    city = models.CharField(max_length=255)
    territory = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255,blank=True,null=True)
    longitude = models.CharField(max_length=255,blank=True,null=True)

class MemberShareContent(models.Model):
    uuid = UUIDField(max_length=36)
    page = models.URLField(max_length=500)
    title = models.CharField(max_length=255,blank=True,null=True)
    image = models.URLField(max_length=500,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    
MEMBER_SHARE_CHOICES = (('pinterest','Share on Pinterest'),('facebook','Share on Facebook'),('google','Share On Google+'),('twitter','Share On Twitter'))
class MemberShare(models.Model):
    uuid = UUIDField(max_length=36)
    member = models.ForeignKey(Member)
    medium = models.CharField(max_length=255,choices=MEMBER_SHARE_CHOICES)
    shared_on = models.DateTimeField(default=datetime.datetime.now())
    content = models.ForeignKey(MemberShareContent)
    


#INSIDERS
"""
class Insider(models.Model):
    user = models.OneToOneField(User)
    joined_on = models.DateTimeField(default=now())
    uuid = UUIDField()
    
    def __unicode__(self):
        return u'%s' % self.user.email
    
    
    def save(self, *args, **kwargs):
        if self.id is None:
             super(Insider, self).save(*args, **kwargs)
             status = InsiderStatus(insider=self,reason="New Insider Registration")
        else:
            super(Insider, self).save(*args, **kwargs)
            
    def get_satus(self):
        try:
            return self.insiderstatus_set.all()[0]
        except:
            return False

class InsiderStatus(models.Model):
    insider = models.ForeignKey(Insider)
    modified = models.DateTimeField(default=now())
    status = models.IntegerField(default=0,choices=((0,'Active'),(1,'Inactive'),(2,'Staff Deactivated')))
    reason = models.TextField(blank=True,null=True)
    
    class Meta:
        ordering = ('-modified',)


class InsiderCampaign(models.Model):
    name=models.CharField(max_length=255)
    uuid = UUIDField()
    description = models.TextField()
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(default=now())
    status = models.IntegerField(default=0)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return reverse('insider_campaign_detail',args=[self.uuid])
    

class InsiderCampaignImage(ImageModel):
    campaign = models.OneToOneField(InsiderCampaign)

from survey.models import Survey
class InsiderCampaignSurvey(models.Model):
    campaign = models.ForeignKey(InsiderCampaign)
    survey = models.ForeignKey(Survey)


class InsiderCampaignApplicant(models.Model):
    insider = models.ForeignKey(Insider)
    campaign = models.ForeignKey(InsiderCampaign)
    requested_on = models.DateTimeField(default=now())
    selected_on = models.DateTimeField(blank=True,null=True)
    selected_by = models.ForeignKey(User,blank=True,null=True)
    
    def is_selected(self):
        if self.selected_on and self.selected_by:
            return True
        return False

class InsiderProductImage(ImageModel):
    title = models.CharField(max_length=255)
    
class InsiderProduct(models.Model):
    image = models.OneToOneField(InsiderProductImage,blank=True,null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)

class InsiderProductCampaign(models.Model):
    campaign = models.ForeignKey(InsiderCampaign)
    product = models.ForeignKey(InsiderProduct)
    
    def get_absolute_url(self):
        return reverse('insider_campaign_product',args=[self.campaign.uuid,self.product.id])
    
    
class InsiderProductStatus(models.Model):
    product = models.ForeignKey(InsiderProduct)
    insider = models.ForeignKey(Insider)
    sent_on = models.DateTimeField(default=datetime.datetime.now())
    recieved_verified_on = models.DateTimeField(blank=True,null=True)

class InsiderProductReview(models.Model):
    product = models.ForeignKey(InsiderProduct)
    reviewed_on = models.DateTimeField(default=datetime.datetime.now())
    insider = models.ForeignKey(Insider)
    rating = models.IntegerField(blank=True,null=True)
    review_title = models.CharField(max_length=255,blank=True,null=True)
    review = models.TextField()
    
    def rating_to_icons(self):
        s = ''
        for r in range(0,self.rating):
            s = u'%s<i class="icon-star "></i>' % s
        return s

#this is user primarily for the Cissonius App, these are users who review products under the basic 'product review' for 
#cissonius but we would like to feature.
class MustHaveContributor(models.Model):
    user = models.OneToOneField(User)
    introduction = models.TextField(blank=True,null=True)
"""
    