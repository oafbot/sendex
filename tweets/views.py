# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
import json, re
import pymongo
from pymongo import MongoClient
import time, datetime

def index(request):
    client = MongoClient('platypo.us:27017')
    db = client.japan
    
    start   = request.GET["start"]
    end     = request.GET["end"]
    keyword = "\\b#?"+request.GET["text"]+"\\b"
            
    data = [t for t in db["posts"].find({'text':{"$regex": keyword, "$options": "-i"}, 
           'timestamp':{"$gte": start, "$lt": end}}, {'_id':0,'text':1,'user.screen_name':1, 
           'id_str':1,'user.profile_image_url':1, 'user.name':1, 'timestamp':1}).sort( "$natural", -1 ).limit(20)]
    
    tweets = [{"tweet":fix_tweet(tweet['text']),
               "url":"http://twitter.com/"+tweet['user']['screen_name']+"/status/"+tweet['id_str'],
               "user":tweet['user']['screen_name'],
               "avatar":tweet['user']['profile_image_url'],
               "id":tweet['id_str'],
               "name":tweet['user']['name'],
               "timestamp":datetime.datetime.strptime(tweet['timestamp'], '%Y-%m-%d %H:%M:%S').strftime("%b %d %Y")}
                for tweet in data]
    
    #st = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M').strftime("%b %d %Y")
    ed = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S').strftime("%b %d %Y")
    
    return render_to_response('tweets/index.html',{"page":"tweets", "tweets":tweets, "topic":request.GET["text"], "end":ed}, context_instance=RequestContext(request))

def tweets(request):    
    client = MongoClient('platypo.us:27017')
    db = client.japan
    
    start   = request.GET["start"]
    end     = request.GET["end"]

    keyword = "\\b#?"+request.GET["text"]+"\\b"
    tweets = [t for t in db["posts"].find({'text':{"$regex": keyword, "$options": "-i"}, 
             'timestamp':{"$gte": start, "$lt": end}}, {'_id':0,'text':1,'user.screen_name':1, 'id_str':1,
             'user.profile_image_url':1, 'user.name':1, 'timestamp':1}).sort( "$natural", -1 )]
    
    #keyword = "\b#?"+request.GET["text"]+"\b"
    #regex   = re.compile(keyword, re.IGNORECASE)
    #tweets = [t for t in db["posts"].find({'text':regex, 'timestamp':{"$gte": start, "$lt": end}}, 
    #         {'_id':0,'text':1,'user.screen_name':1, 'id_str':1,
    #          'user.profile_image_url':1, 'user.name':1, 'timestamp':1}).sort( "$natural", -1 )]

    data = [{"tweet":fix_tweet(tweet['text']),
             "url":"http://twitter.com/"+tweet['user']['screen_name']+"/status/"+tweet['id_str'], 
             "user":tweet['user']['screen_name'], 
             "avatar":tweet['user']['profile_image_url'], 
             "id":tweet['id_str'],
             "name":tweet['user']['name'],
             "timestamp":datetime.datetime.strptime(tweet['timestamp'], '%Y-%m-%d %H:%M:%S').strftime("%b %d %Y")}
             for tweet in tweets]
    
    return HttpResponse(json.dumps(data), content_type='application/json')


def fix_tweet(text):
    import re
    urls = re.compile("(?P<url>https?://[^\s]+)")
    mentions = re.compile('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z_]+[A-Za-z0-9_]+)')
    hashtags = re.compile('(?<=^|(?<=[^a-zA-Z0-9-\.]))#([A-Za-z_]+[A-Za-z0-9_]+)')
    
    text = urls.sub(r'<a href="\1" target=_blank>\1</a>', text)
    text = mentions.sub(r'<a href=http://www.twitter.com/\1 target=_blank class=user>@\1</a>', text)
    text = hashtags.sub(r'<a href=https://twitter.com/search?q=\1 target=_blank class=hash>#\1</a>', text)
    return text