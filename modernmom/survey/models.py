from django.db import models
from django.core.exceptions import ValidationError
from fields import UUIDField
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils import timezone


class Survey(models.Model):
	name = models.CharField(max_length=400)
	description = models.TextField()
	uuid = UUIDField()

	def __unicode__(self):
		return (self.name)

	
class Choice(models.Model):
	choice = models.TextField()

	def __unicode__(self):
		return u'%s' % self.choice
			
class Question(models.Model):
	survey = models.ForeignKey(Survey)
	question = models.TextField()
	uuid = UUIDField()
	is_required = models.BooleanField(default=True)
	ordering = models.IntegerField(default=-1)
	
	def __unicode__(self):
		return u'%s' % self.question
		
		
	def has_choices(self):
		if self.questionchoice_set.count() > 0:
			return True
		return False
	
	def get_choices(self):
		choices = [(str(cc.choice.id),str(cc.choice.choice)) for cc in self.questionchoice_set.all()]
		return choices

class QuestionChoice(models.Model):
	question = models.ForeignKey(Question)
	choice = models.ForeignKey(Choice)
	ordering = models.IntegerField(default=0)
	class Meta:
		ordering = ('ordering','-id')

class QuestionChoiceWeight(models.Model):
	questionchoice = models.OneToOneField(QuestionChoice)
	weight = models.IntegerField()

class Response(models.Model):
	question = models.ForeignKey(Question)
	user = models.ForeignKey(User)
	text = models.TextField(blank=True,null=True)
	choice = models.ForeignKey(Choice,blank=True,null=True)
	answered_on = models.DateTimeField(default=timezone.now())
	
	

	








