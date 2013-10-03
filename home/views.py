# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
import json, datetime

def index(request):
    now   = datetime.datetime.utcnow()
    start = (now + datetime.timedelta(days=-2)).strftime("%Y-%m-%d %H:%M")
    end   = now.strftime("%Y-%m-%d %H:%M")
    
    return render_to_response('home/index.html',{"page":"home", "start":start, "end":end}, context_instance=RequestContext(request))

    
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

def worldmap(request):
    import pymongo
    from pymongo import MongoClient
    from collections import Counter
    
    query = {}
    client = MongoClient('platypo.us:27017')
    db = client.japan
    
    for param, val in request.GET.iteritems():
        if param == "start":
           start = val
        elif param == "end":
           end = val
        elif param == "text":
            keyword = val

    timezone = [u['user']["time_zone"] for u in db["posts"].find({'user.time_zone':{"$ne" : ""}, 
               'timestamp':{"$gte": start, "$lt": end}}, {'_id':0,'user.time_zone':1})]
    
    timezone = filter(None, timezone)
    counts = Counter(timezone)
    locations = sorted(counts.iteritems(), key=lambda x: x[1], reverse=True)
    
    data = [{"name":loc[0].replace(" ", "_").replace("(", "_x28_").replace(")", "_x29_").replace("&", "_x26_").replace("'", "_x27_"),"size":2+loc[1]/5} for loc in locations]
    
    return HttpResponse(json.dumps(data), content_type='application/json')
    

def tweets(request):
    import pymongo
    from pymongo import MongoClient
    
    client = MongoClient('platypo.us:27017')
    db = client.japan
    
    for param, val in request.GET.iteritems():
        if param == "start":
           start = val
        elif param == "end":
           end = val
        elif param == "text":
            keyword = val
        
    tweets = [t for t in db["posts"].find({'text':{"$regex": keyword}, 
              'timestamp':{"$gte": start, "$lt": end}}, {'_id':0,'text':1,'user.screen_name':1, 'id_str':1})]

    data = [{"tweet":tweet['text'],"url":"http://twitter.com/"+tweet['user']['screen_name']+"/status/"+tweet['id_str']} for tweet in tweets]
    
    return HttpResponse(json.dumps(data), content_type='application/json')
            
