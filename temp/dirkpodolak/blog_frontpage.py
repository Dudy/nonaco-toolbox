######################################################################################################
# blog frontpage
######################################################################################################

import jinja_worker
import user_handling
import blogentry
import json
import time
import logging

from google.appengine.ext import db
from google.appengine.api import memcache

memcachekey_blog = 'blog'
dirties = { 0:True } # 0 = main page, other number = permalink
last_query_times = { 0:0 } # 0 = main page, other number = permalink

class Handler_blog_frontpage(jinja_worker.Handler_jinja_worker):
    def get(self):
        global dirties
        global last_query_times
        global memcachekey_blog
        
        username = user_handling.get_username_from_cookie(self)
        
        blogentries = memcache.get(memcachekey_blog)
        if blogentries is None or dirties[0] is None or dirties[0] == True:
            blogentries = db.GqlQuery("select * from Blogentry order by created desc limit 10")
            blogentries = list(blogentries)
            memcache.set(memcachekey_blog, blogentries)
            last_query_times[0] = time.time()
            age = 0
            dirties[0] = False
        else:
            age = int(time.time() - last_query_times[0])
        
        if username:
            self.render("front.html", blogentries = blogentries, username = username, age = age)
        else:
            self.render("frontpage.html", blogentries = blogentries, username = username, age = age)

    def post(self):
        if self.request.get("signup"):
            self.redirect("/blog/signup")
        elif self.request.get("login"):
            self.redirect("/blog/login")
        elif self.request.get("logout"):
            self.redirect("/blog/logout")
        elif self.request.get("newpost"):
            self.redirect("/blog/newpost")

class Handler_blog_newpost(jinja_worker.Handler_jinja_worker):
    def get(self):
        username = user_handling.get_username_from_cookie(self)
        self.render("newpost.html", username = username)
    
    def post(self):
        global dirties
        
        username = user_handling.get_username_from_cookie(self)
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            a = blogentry.Blogentry(subject = subject, content = content)
            a.put()
            dirties[0] = True
            
            self.redirect("/blog/" + str(a.key().id()))
        else:
            error = "we need both a subject and some content!"
            self.render("newpost.html", subject = subject, content = content, error = error, username = username)

class Handler_blog_permalink(jinja_worker.Handler_jinja_worker):
    def get(self, id):
        global dirties
        global last_query_times
        
        username = user_handling.get_username_from_cookie(self)
        
        int_id = int(id)
        be = memcache.get('permalink_' + id)
        
        if be is None or dirties.get(int_id) is None or dirties.get(int_id) == True:
            logging.error("load")
            be = blogentry.Blogentry.get_by_id(int_id)
            memcache.set('permalink_' + id, be)
            last_query_times[int_id] = time.time()
            age = 0
            dirties[int_id] = False
            logging.error("dirties[int_id] = " + str(dirties[int_id]))
        else:
            logging.error("don't load")
            if not last_query_times.get(int_id):
                last_query_times[int_id] = time.time()
            age = int(time.time() - last_query_times.get(int_id))
        
        self.render("permalink.html", blogentry = be, username = username, age = age)

    def post(self, id):
        if self.request.get("logout"):
            self.redirect("/blog/logout")
        elif self.request.get("newpost"):
            self.redirect("/blog/newpost")

class Handler_blog_json(jinja_worker.Handler_jinja_worker):
    def get(self, id = None):
        json_output = ""
        
        if id:
            be = blogentry.Blogentry.get_by_id(int(id))
            json_output = "[" + be.get_json() + "]"
        else:
            json_output = "["
            blogentries = db.GqlQuery("select * from Blogentry order by created desc limit 10")
            blogentries = list(blogentries)
 
# auch eine Moeglichkeit, im Forum gefunden: http://forums.udacity.com/cs253-april2012/questions/21869/lost-in-hw-5
#            json_output = [{'subject': blogentry.title,
#                            'content': blogentry.post,
#                            'created': str(blogentry.created.strftime('%a %b %d %H:%M:%S %Y')),
#                            'last_modified': str(blogentry.last_modified.strftime('%a %b %d %H:%M:%S %Y'))
#                           } for blogentry in blogentries]
            
            for be in blogentries:
                json_output += be.get_json() + ','
            json_output = json_output[0:-1] + "]"
            
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.response.out.write(json.dumps(json_output))

class Handler_blog_flush(jinja_worker.Handler_jinja_worker):
    def get(self):
        global dirties
        for d in dirties:
            dirties[d] = True
        memcache.flush_all()
        self.redirect('/blog')