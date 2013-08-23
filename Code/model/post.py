from google.appengine.api import users
from google.appengine.ext import ndb

POST_LIST_DB_KEY_NAME = 'post_list_db_key'

class Post(ndb.Model):
    author = ndb.UserProperty(required = True)
    content = ndb.TextProperty(indexed=False, required = True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def post_db_key(self):
        return ndb.Key('Post', POST_LIST_DB_KEY_NAME)