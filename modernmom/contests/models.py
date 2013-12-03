from django.db import models

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()
    
from photologue.models import ImageModel
import datetime
from django.core.urlresolvers import reverse
from photologue.models import ImageModel
from fields import UUIDField
from django.db.models import Q

    
class ContestManager(models.Manager):
    #def get_query_set(self):
    #    return super(ActiveContestManager, self).get_query_set().filter(status=1)
    
    def active(self):
        """
        Retrieves all active articles which have been published and have not
        yet expired.
        """
        now = datetime.datetime.now()
        return self.get_query_set().filter(
                Q(ends_on__isnull=True) |
                Q(ends_on__gte=now),
                starts_on__lte=now,
                status=1)

    
class Contest(models.Model):
    name = models.CharField(max_length=255)
    guid = UUIDField(max_length=36)
    url = models.SlugField(max_length=255)
    status = models.IntegerField(default=0,choices=((0,'Draft'),(1,'Active'),(2,'Inactive')))
    starts_on = models.DateTimeField(default=datetime.datetime.now())
    ends_on = models.DateTimeField(default=datetime.datetime.now())
    entries_per_day = models.IntegerField(default=0)
    total_entry_count = models.IntegerField(default=1)
    objects = ContestManager()
    #active = ActiveContestManager()
    
    def is_expired(self):
        if self.status == 2:
            return True
        return False
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_absolute_url(self):
        return reverse('contest_detail',args=[self.url])
    
    def get_report_url(self):
        return reverse('contest_report',args=[self.url])
    
    def get_share_url(self):
        return reverse('share_contest',args=[self.url])

#from django.db.models.signals import post_save


def do_something(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    obj = kwargs['instance']
    print 'the object is now saved.'
    # ...do something else...

# here we connect a post_save signal for MyModel
# in other terms whenever an instance of MyModel is saved
# the 'do_something' function will be called.
#post_save.connect(do_something, sender=MyModel)

class ContestDescription(models.Model):
    contest = models.OneToOneField(Contest)
    content = models.TextField()
    
    def __unicode__(self):
        return u'%s' % self.content

class ContestImage(ImageModel):
    contest = models.OneToOneField(Contest)

class Contestant(models.Model):
    email = models.EmailField(max_length=255)
    
    def __unicode__(self):
        return u'%s' % self.email
    
class ContestantEntry(models.Model):
    contestant = models.ForeignKey(Contestant)
    contest = models.ForeignKey(Contest)
    entered_on = models.DateTimeField(default=datetime.datetime.now())
    ip_address = models.CharField(max_length=50)

class ContestantEntryImage(ImageModel):
    contestantentry = models.ForeignKey(ContestantEntry)
    
class ContestantEntryKey(models.Model):
    contestantentry = models.ForeignKey(ContestantEntry)
    entry_key = models.CharField(max_length=255)
    entry_value = models.CharField(max_length=255)

SHARE_CHOICES = ((0,'Facebook'),(1,'Twitter'),(2,'Pinterest'))
class ContestantShare(models.Model):
    contestant = models.ForeignKey(Contestant)
    contest = models.ForeignKey(Contest)
    shared_at = models.DateTimeField(default=datetime.datetime.now())
    shared_on = models.IntegerField(choices=SHARE_CHOICES)

    
class ContestantEntryWinner(models.Model):
    contestantentry = models.ForeignKey(ContestantEntry)
    chosen_on=models.DateTimeField(default=datetime.datetime.now())
    chosen_by = models.ForeignKey(User)

class AcceptedContestantEntryWinner(models.Model):
    contestantentrywinner = models.OneToOneField(ContestantEntryWinner)
    accepted_prize = models.BooleanField(default=True)
    accepted_on = models.DateTimeField(default=datetime.datetime.now())
    accepted_by = models.ForeignKey(User)
    notes = models.TextField()
    




    
