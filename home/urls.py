from django.conf.urls import patterns, url
from home import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^cloud/$', views.cloud),
    url(r'^graph/$', views.graph),
    url(r'^map/$', views.worldmap),
    url(r'^tweets/$', views.tweets)
)
