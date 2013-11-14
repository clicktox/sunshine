from survey.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class QuestionInline(admin.TabularInline):
	model = Question
	extra = 0


class SurveyAdmin(admin.ModelAdmin):
	inlines = [QuestionInline,]

admin.site.register(Survey, SurveyAdmin)

class QuestionChoiceInline(admin.TabularInline):
	model = QuestionChoice
	extra = 0
class QuestionAdmin(admin.ModelAdmin):
	inlines = [QuestionChoiceInline,]
admin.site.register(Question, QuestionAdmin)

class QuestionChoiceWeightInline(admin.TabularInline):
	model = QuestionChoiceWeight
	extra = 0
	
class QuestionChoiceAdmin(admin.ModelAdmin):
	inlines = [QuestionChoiceWeightInline,]
	list_display = ('question','choice')
	list_filter = ('question',)
admin.site.register(QuestionChoice,QuestionChoiceAdmin)
admin.site.register(Choice)

class ResponseAdmin(admin.ModelAdmin):
	list_display = ('user','question','text','choice')
	readonly_fields = ('user','text','question','choice')
admin.site.register(Response, ResponseAdmin)