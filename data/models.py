# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
# python manage.py inspectdb --database=jpndex > data/models.py

from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from multi_db_model_admin import MultiDBModelAdmin
from multi_db_tabular_inline import MultiDBTabularInline

class Jpndex(models.Model):
    id = models.IntegerField(primary_key=True)
    stamp = models.DateTimeField()
    jpndex = models.FloatField()
    volume = models.IntegerField()
    class Meta:
        db_table = 'jpndex'
        app_label = 'data'
        
    def json(self):
        from collections import OrderedDict
        return OrderedDict((
            ('time' , str(self.stamp)[:-9]),
            ('jpndex', self.jpndex),
            ('volume', self.volume)
        ))
        
    def __unicode__(self):
        return str(self.id)

class Wordcloud(models.Model):
    id = models.IntegerField(primary_key=True)
    stamp = models.DateTimeField()
    term = models.CharField(max_length=64L)
    frequency = models.IntegerField()
    class Meta:
        db_table = 'wordcloud'
        app_label = 'data'

    def json(self):
        from collections import OrderedDict
        return OrderedDict((
            # ('time', str(self.stamp)[:-9]),
            ('term', self.term),
            ('frequency', self.frequency)
        ))
        
    def __unicode__(self):
        return str(self.id)    
        
class Predictor(models.Model):
    id = models.IntegerField(primary_key=True)
    stamp = models.DateTimeField()
    term = models.CharField(max_length=128L)
    classification = models.CharField(max_length=8L)
    class Meta:
        db_table = 'predictors'
        app_label = 'data'

    def json(self):
        from collections import OrderedDict
        return OrderedDict((
            ('term', self.term),
            ('classification', self.classification)
        ))
    
    def __unicode__(self):
        return str(self.id)
        

 
# # Specialize the multi-db admin objects for use with specific models.
class PredictorAdmin(MultiDBModelAdmin):
    list_display = ('id', 'stamp', 'term', 'classification') 

class WordcloudAdmin(MultiDBModelAdmin):
    list_display = ('id', 'stamp', 'term', 'frequency')

class SendexAdmin(MultiDBModelAdmin):
    list_display = ('id', 'stamp', 'jpndex', 'volume')
    
admin.site.register(Predictor, PredictorAdmin)
admin.site.register(Wordcloud, WordcloudAdmin)
admin.site.register(Jpndex, SendexAdmin)

