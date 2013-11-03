from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from jpndex import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jpndex.views.home', name='home'),
    # url(r'^jpndex/', include('jpndex.foo.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^home/', include('home.urls')),
    url(r'^tweets/', include('tweets.urls')),
    url(r'^data/', include('data.urls')),
)
urlpatterns += staticfiles_urlpatterns()