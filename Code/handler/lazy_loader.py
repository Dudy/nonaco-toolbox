﻿import json
import jinja_worker
import os, sys
import datetime as dt

from google.appengine.api import users
from google.appengine.ext import ndb

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

from post import Post

class Handler_lazy_loader(jinja_worker.Handler_jinja_worker):
    def get(self, urlString = None):
        if urlString:
            user = users.get_current_user()
            
            if user:
                rev_key = ndb.Key(urlsafe=urlString)
                last_post = rev_key.get()

                post_query = Post.query(Post.created < last_post.created, ancestor = Post.post_db_key()).order(-Post.created)
                post_list = post_query.fetch(10)
                
                if len(post_list) > 0:
                    urlString = post_list[len(post_list) - 1].key.urlsafe()
                
                posts = []
                for post in post_list:
                    dict = { 'nickname': post.author.nickname(), 'content': post.content, 'created': post.created.strftime("%d.%m.%Y %H:%M:%S") }
                    posts.append(dict)
                post_dict = { 'urlString': urlString, 'posts': posts }
                
                self.response.write(json.dumps(post_dict))
            else:
                self.response.write('{ "message": "please log in" }')