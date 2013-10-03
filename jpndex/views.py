from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
import datetime

def index(request):
    # return HttpResponse("Hello World")
    # redirect('home.views.index')
    now   = datetime.datetime.utcnow()
    end   = (now + datetime.timedelta(hours=-1))
    start = (end + datetime.timedelta(days=-2)).strftime("%Y-%m-%d %H:%M")
    end = end.strftime("%Y-%m-%d %H:%M")
    
    return render_to_response('home/index.html',{"page":"home", "start":start, "end":end}, context_instance=RequestContext(request))
