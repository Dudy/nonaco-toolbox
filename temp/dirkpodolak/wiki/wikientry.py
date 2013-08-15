from google.appengine.ext import db

class Wikientry(db.Model):
    url = db.StringProperty(required = True)
    content = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add = True)
