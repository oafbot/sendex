from django.db import connections

class DBRouter(object):
    """A router to control all database operations on models in
    the data application"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'data':
            return 'data'        
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'data':
            return 'data'        
        return None

    def allow_syncdb(self, db, model):
        "Make sure syncdb doesn't run on anything but default"
        if model._meta.app_label == 'data':
            return False
        elif db == 'default':
            return True
        return None