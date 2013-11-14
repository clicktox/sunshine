from django.db import models
from fields import UUIDField

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class TwitterProfile(models.Model):
    
    id = models.BigIntegerField(primary_key=True)
    screen_name = models.CharField(u'Screen name', max_length=50, unique=True)
    uuid = UUIDField()
    name = models.CharField(u'Name', max_length=100,blank=True,null=True)
    location = models.CharField(u'Location', max_length=100,blank=True,null=True)
    raw =models.TextField()

   
    def __unicode__(self):
        return self.name

    def get_url(self):
        return 'https://twitter.com/%s' % self.screen_name


class Application(models.Model):
    name = models.CharField(max_length=255)
    appid = models.BigIntegerField()
    consumer_key = models.CharField(max_length=500)
    consumer_secret = models.CharField(max_length=500)
    
    def get_authorize_url(self):
        return reverse('twitter_authorize_url', args=[self.appid])
    
    

class UserApplicationAccess(models.Model):
    application = models.ForeignKey(Application)
    user = models.ForeignKey(User)
    access_token = models.CharField(max_length=500)
    access_token_secret = models.CharField(max_length=500)
    profile = models.OneToOneField(TwitterProfile,blank=True,null=True)
    
    def __unicode__(self):
        return u'%s : %s' % (self.profile.screen_name,self.application.name)

    def get_last_fetch_id(self):
        try:
            return self.Tweet_set.objects.all().order_by('-tweet_id')[0].tweet_id
        except:
            return -1
    
    def fetch_tweets(self):
        pass
        
        
class Tweet(models.Model):
    raw = models.TextField()
    tweet_id = models.BigIntegerField()
    application = models.ForeignKey(UserApplicationAccess)
    

