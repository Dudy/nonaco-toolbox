import json
import datetime
import jinja_worker
import os, sys

from google.appengine.api import users
from google.appengine.ext import ndb

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

from post import Post

class Handler_homepage(jinja_worker.Handler_jinja_worker):
    def get(self):
        user = users.get_current_user()
        posts = self.get_posts()
        
        if len(posts) > 0:
            urlString = posts[len(posts) - 1].key.urlsafe()
        
        if user:
            self.render("homepage.html", username = user.nickname(), url = users.create_logout_url('/'), posts = posts, urlString = urlString)
        else:
            self.render("homepage.html", username = None, url = users.create_login_url('/'))
    
    def post(self):
        user = users.get_current_user()
        
        if user:
            post = Post(parent = Post.post_db_key(), author_id = user.user_id(), content = self.request.get("content"))
            post.put()
            self.redirect('/')

    def get_posts(self):
        user = users.get_current_user()
        post_list = []
        
        if user:
            post_query = Post.query(ancestor = Post.post_db_key()).order(-Post.created)
            post_list = post_query.fetch(10)
            
            if len(post_list) == 0:
                post = Post(parent = Post.post_db_key(), author_id = user.user_id(), content = 'Hallo Leute! Hier ist mal eine allererste Version des Kollaborationswerkzeugs, ich nenne das erst mal einfach nur <b>Toolbox</b>. In dieser ersten Version kann man allerdings noch nichts machen, ich arbeite dran ;-) Schaut euch die Seite zwei, drei mal am Tag an, ich will z&uuml;gig Ergebnisse liefern.')
                post.put()
                
                post_query = Post.query(ancestor = Post.post_db_key()).order(-Post.created)
                post_list = post_query.fetch(10)
        
        return post_list
