from django.db import models
from fields import UUIDField
from photologue.models import ImageModel
from fields import UUIDField
from django_twitter.models import UserApplicationAccess
import datetime

class ScoopImage(ImageModel):
    pass

class ScoopItem(models.Model):
    name = models.CharField(max_length=255)
    uuid = UUIDField()
    tease = models.TextField()
    description = models.TextField()

class ScoopTopic(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,unique=True)
    uuid = UUIDField()
    tease = models.TextField()
    description = models.TextField()
    image = models.OneToOneField(ScoopImage,blank=True,null=True)

class ScoopTopicTwitter(models.Model):
    topic = models.ForeignKey(ScoopTopic)
    applicationaccess = models.ForeignKey(UserApplicationAccess)

class ScoopTopicItem(models.Model):
    item = models.ForeignKey(ScoopItem)
    topic = models.ForeignKey(ScoopTopic)
    publish_date = models.DateField(default=datetime.date.today())
    priority = models.IntegerField(default=0)

class ScoopTweet(models.Model):
    #crawls ScoopTopicTwitter
    raw_tweet = models.TextField()
    tweet_id = models.BigIntegerField()
    tweeter = models.CharField(max_length=255)
    status = models.IntegerField(default=0,choices=((0,'Fresh'),(1,'Do Not Display')))
    
class ScoopItemTweet(models.Model):
    tweet = models.ForeignKey(ScoopTweet)
    status = models.IntegerField(default=0,choices=((0,'Fresh'),(1,'Do Not Display')))
    