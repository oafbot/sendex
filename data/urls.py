from django.conf.urls import patterns, url
from data import views

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    url(r'^cloud/$', views.cloud),
    url(r'^graph/$', views.graph),
    url(r'^informative/$', views.informative)
)
