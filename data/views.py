# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
import json, datetime


def cloud(request):
    query = {}
    cloud = Wordcloud.objects
    
    for param, val in request.GET.iteritems():
        if param == "start":
            cloud = cloud.filter(stamp__gte=val)
        elif param == "end":
            cloud = cloud.filter(stamp__lt=val)
        else:
            query[param] = val
    
    data = [wc.json() for wc in cloud.filter(**query).order_by('id')]
    
    return HttpResponse(json.dumps(data), content_type='application/json')
    
        
def graph(request):
    query = {}
    jpndex = Jpndex.objects
    
    for param, val in request.GET.iteritems():    
        if param == "start":
            jpndex = jpndex.filter(stamp__gte=val)
        elif param == "end":
            jpndex = jpndex.filter(stamp__lt=val)
        else:
            query[param] = val
    
    data = [jpn.json() for jpn in jpndex.filter(**query).order_by('id')]    
    
    return HttpResponse(json.dumps(data), content_type='application/json')

def informative(request):
    query = {}
    predict = Predictor.objects
    
    for param, val in request.GET.iteritems():    
        if param == "start":
            predict = predict.filter(stamp__gte=val)
        elif param == "end":
            predict = predict.filter(stamp__lt=val)
        else:
            query[param] = val
    
    data = [info.json() for info in predict.filter(**query).order_by('id')]    
    
    return HttpResponse(json.dumps(data), content_type='application/json')