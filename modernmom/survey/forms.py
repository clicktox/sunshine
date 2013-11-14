from django import forms
from django.forms import models
from survey.models import *
from django.utils.safestring import mark_safe
import uuid

# blatantly stolen from 
# http://stackoverflow.com/questions/5935546/align-radio-buttons-horizontally-in-django-forms?rq=1
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))



class SurveyForm(forms.Form):
   
    def __init__(self, *args, **kwargs):
        # expects a survey object to be passed in initially
        survey = kwargs.pop('survey')
        self.survey = survey
        user = kwargs.pop('user')
        self.user = user
        super(SurveyForm, self).__init__(*args, **kwargs)
        #self.uuid = random_uuid = uuid.uuid4().hex    

        # add a field for each survey question, corresponding to the question
        # type as appropriate.
        
        data = kwargs.get('data')
        qcount = survey.question_set.count()
        rcount = 0
        for q in survey.question_set.all():
            try:
                has_answerd = Response.objects.get(question=q,user=self.user)
                rcount = rcount+1
            except Response.DoesNotExist:
                if q.has_choices():
                    self.fields["question_%s" % q.uuid] = forms.ChoiceField(label=q.question, 
                        widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), 
                        choices = q.get_choices())
                else:
                    self.fields["question_%s" % q.uuid] = forms.CharField(label=q.question, 
                        widget=forms.Textarea)
                self.fields["question_%s" % q.uuid].required = False
                # if the field is required, give it a corresponding css class.
                """
                if q.required:
                    self.fields["question_%d" % q.pk].required = True
                    self.fields["question_%d" % q.pk].widget.attrs["class"] = "required"
                else:
                    self.fields["question_%d" % q.pk].required = False
                """
                        # initialize the form field with values from a POST request, if any.
            if data:
                self.fields["question_%d" % q.uuid].initial = data.get('question_%d' % q.uuid)
        self.questions_left = qcount-rcount
    
    def save(self):
        message = []
        for field_name, field_value in self.cleaned_data.iteritems():
            if field_name.startswith("question_"):
                if len(field_value) > 0: 
                    q_uuid = field_name.split("_")[1]
                    q = Question.objects.get(uuid=q_uuid)
                    if q.has_choices():
                        response,c = Response.objects.get_or_create(question=q,user=self.user,defaults={'choice':Choice.objects.get(id=int(field_value)),})
                    else:
                        response,c = Response.objects.get_or_create(question=q,user=self.user,defaults={'text':field_value,})                                             
                    message.append( u'%s:%s<br>%s: %s | %s' % (field_name,field_value,response.question,response.text, response.choice) )
        return message
    
       


