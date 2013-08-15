from google.appengine.ext import db

class Blogentry(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    
    def get_json(self):
        return '{"content": "' + self.content + '", "subject": "' + self.subject + '"}'