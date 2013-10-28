from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.utils.timezone import utc
import datetime
from data.models import Jpndex

def index(request):
    # redirect('home.views.index')
    now   = datetime.datetime.utcnow().replace(minute=0, second=0, microsecond=0, tzinfo=utc)
    end   = (now + datetime.timedelta(hours=-1))
    start = (end + datetime.timedelta(days=-2)).strftime("%Y-%m-%d %H:%M:%S")
    end   = end.strftime("%Y-%m-%d %H:%M:%S")
    sndx  = Jpndex.objects.order_by('id').reverse()[0]
    
    return render_to_response('home/index.html',{"page":"home", "start":start, "end":end, "sndx":sndx.jpndex}, 
    context_instance=RequestContext(request))
