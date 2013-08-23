import json
import datetime
import jinja_worker
import os, sys
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

from post import Post

class Handler_postings(jinja_worker.Handler_jinja_worker):
    def get(self):
        user = users.get_current_user()
        posts = self.get_posts()
        
        if len(posts) > 0:
            urlString = posts[len(posts) - 1].key.urlsafe()
        
        if user:
            html_text = self.render_str("dynamic/postings.body.html", posts = posts)
            requirement_dict = { 'content': html_text }
            self.response.write(json.dumps(requirement_dict))
        else:
            self.render("postings.html", username = None, url = users.create_login_url('/'))
    
    def post(self):
        user = users.get_current_user()
        
        if user:
            post = Post(parent = Post.post_db_key(), author = user, content = self.request.get("content"))
            post.put()
            requirement_dict = { 'success': True, 'content': post.content, 'created': post.created.strftime("%d.%m.%Y %H:%M:%S"), 'user': user.nickname() }
            self.response.write(json.dumps(requirement_dict))
        else:
            requirement_dict = { 'success': False, 'message': 'not logged in' }
            self.response.write(json.dumps(requirement_dict))

    def get_posts(self):
        user = users.get_current_user()
        post_list = []
        
        post_query = Post.query(ancestor = Post.post_db_key()).order(-Post.created)
        post_list = post_query.fetch(10)
        
        if user and len(post_list) == 0:
            #post = Post(parent = Post.post_db_key(), author = user, content = 'Hallo Leute! Hier ist mal eine allererste Version des Kollaborationswerkzeugs, ich nenne das erst mal einfach nur <b>Toolbox</b>. In dieser ersten Version kann man allerdings noch nichts machen, ich arbeite dran ;-) Schaut euch die Seite zwei, drei mal am Tag an, ich will zügig Ergebnisse liefern.')
            #post.put()
            
            post = Post(parent = Post.post_db_key(), author = user, content = 'Bugreport #2: Leere Posts sind möglich, siehe meinen Vorherigen', created = datetime.datetime(year = 2013, month = 8, day = 20, hour = 18, minute = 51, second = 38))
            post.put()
            
            post = Post(parent = Post.post_db_key(), author = user, content = '', created = datetime.datetime(year = 2013, month = 8, day = 20, hour = 18, minute = 51, second = 13))
            post.put()
            
            post = Post(parent = Post.post_db_key(), author = user, content = 'Bugreport #1: Als Verfasser wird mein Name und nicht deiner angezeigt, Dirk!', created = datetime.datetime(year = 2013, month = 8, day = 20, hour = 18, minute = 50, second = 48))
            post.put()
            
            post = Post(parent = Post.post_db_key(), author = user, content = 'Hi. Heute hab ich dieses Nachrichtenfeature fertig gemacht. Wir können uns jetzt, so ähnlich wie bei Facebook, Nachrichten an diese Pinwand posten. Als nächstes gehe ich an das eigentliche Projektmanagement.', created = datetime.datetime(year = 2013, month = 8, day = 19, hour = 7, minute = 58, second = 58))
            post.put()
            post = Post(parent = Post.post_db_key(), author = user, content = 'Hallo Leute! Hier ist mal eine allererste Version des Kollaborationswerkzeugs, ich nenne das erst mal einfach nur <b>Toolbox</b>. In dieser ersten Version kann man allerdings noch nichts machen, ich arbeite dran ;-) Schaut euch die Seite zwei, drei mal am Tag an, ich will z&uuml;gig Ergebnisse liefern.', created = datetime.datetime(year = 2013, month = 8, day = 19, hour = 6, minute = 37, second = 32))
            post.put()
            
            post_query = Post.query(ancestor = Post.post_db_key()).order(-Post.created)
            post_list = post_query.fetch(10)
        
        return post_list
