from google.appengine.ext import db
from google.appengine.api import memcache

import logging
import helpers

class KeyValue(db.Model):
    k = db.StringProperty(required=True)
    v = db.StringProperty(required=True)
    
    @classmethod
    def get(cls, key, default=None):
        r = cls.all().filter('k =', key).get()
        if r:
            return r.v
        return default

    @classmethod
    def set(cls, key, value=None):
        r = cls.all().filter('k =', key).get()
        if r:
            r.v = value
            r.save()
            return r
        obj = cls(k=key, v=value)
        obj.save()
        return obj
