# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
# from __future__ import unicode_literals
# 
# from django.db import models
# 
# class Jpndex(models.Model):
#     id = models.IntegerField(primary_key=True)
#     stamp = models.DateTimeField()
#     jpndex = models.FloatField()
#     volume = models.IntegerField()
#     class Meta:
#         db_table = 'jpndex'
#     
#     def json(self):
#         from collections import OrderedDict
#         #import ordereddict as OrderedDict
#         return OrderedDict((
#             ('time', str(self.stamp)[:-9]),
#             ('jpndex', self.jpndex),
#             ('volume', self.volume)
#         ))
# 
# 
# class Wordcloud(models.Model):
#     id = models.IntegerField(primary_key=True)
#     stamp = models.DateTimeField()
#     term = models.CharField(max_length=64L)
#     frequency = models.IntegerField()
#     class Meta:
#         db_table = 'wordcloud'
# 
#     def json(self):
#         from collections import OrderedDict
#         #import ordereddict as OrderedDict
#         return OrderedDict((
#             # ('time', str(self.stamp)[:-9]),
#             ('term', self.term),
#             ('frequency', self.frequency)
#         ))

