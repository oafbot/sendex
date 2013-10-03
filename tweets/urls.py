from django.conf.urls import patterns, url
from tweets import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^tweets/$', views.tweets)
)
