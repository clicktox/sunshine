from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
import datetime
import settings
from models import *
from operator import itemgetter
from django.core.exceptions import PermissionDenied
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def survey_list(request,template='survey/list.html'):
    context={}
    context['surveys'] = Survey.objects.all()
    return render_to_response(template,context,context_instance=RequestContext(request))
@staff_member_required
def survey_results_weighted(request,survey_id,template='survey/results/weighted.html'):
    context={}
    context['survey'] = survey = get_object_or_404(Survey,id=survey_id)
    #get all the questions for survey
    questions = survey.question_set.all()
    context['results'] = []
    context['users'] = {}
    for q in questions:
        if q.has_choices():
            for choice in q.questionchoice_set.all():
                try:
                    weight = choice.questionchoiceweight.weight
                    user_count = choice.choice.response_set.count()
                    user_set = choice.choice.response_set.filter(question=q)
                    context['results'].append({'question':q,'choice':choice.choice,'count':user_count})
                    for u in user_set:
                        if u.user not in context['users']:
                            context['users'][u.user] = weight
                        else:
                            context['users'][u.user] = context['users'][u.user]+weight
                except QuestionChoiceWeight.DoesNotExist:
                    pass
    context['users_list'] = sorted(context['users'].items(), key=lambda x: x[1], reverse=True)
    return render_to_response(template,context,context_instance=RequestContext(request))


@staff_member_required
def survey_results_user(request,survey_id,user_id,template='survey/results/user.html'):
    context={}
    responses = []
    context['survey'] = survey = get_object_or_404(Survey,id=survey_id)
    context['oUser'] = user = get_object_or_404(User,id=user_id)
    #get all the questions for survey
    questions = survey.question_set.all()
    for q in questions:
        responses.append({'question':q,'response':Response.objects.get(question=q,user=user)})
    context['responses'] = responses
    return render_to_response(template,context,context_instance=RequestContext(request))